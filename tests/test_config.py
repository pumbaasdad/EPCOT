"""Tests for the config module."""

import pytest
from pathlib import Path
import tempfile
import yaml
from typing import Dict, Any, Generator

from epcot.config import (
    load_config, get_figments, get_figment_config, process_template_values
)


@pytest.fixture
def sample_config() -> Dict[str, Any]:
    """Create a sample configuration for testing."""
    return {
        "figments": [
            "backup",
            "certificates",
            "dhcp",
            {"reverse-proxy": {"certificate_volume_name": "cert_vol"}},
            {"transcode": {"source_volume_name": "media_vol"}},
        ]
    }


@pytest.fixture
def config_file(sample_config: Dict[str, Any]) -> Path:
    """Create a temporary config file for testing."""
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w") as temp:
        yaml.dump(sample_config, temp)
        return Path(temp.name)


def test_load_config(config_file: Path) -> None:
    """Test loading a configuration file."""
    config = load_config(config_file)
    assert "figments" in config
    assert len(config["figments"]) == 5


def test_load_config_file_not_found() -> None:
    """Test loading a non-existent configuration file."""
    with pytest.raises(FileNotFoundError):
        load_config(Path("non_existent_file.yaml"))


def test_get_figments(sample_config: Dict[str, Any]) -> None:
    """Test extracting figment names from a configuration."""
    figments = get_figments(sample_config)
    assert len(figments) == 5
    assert "backup" in figments
    assert "certificates" in figments
    assert "dhcp" in figments
    assert "reverse-proxy" in figments
    assert "transcode" in figments


def test_get_figments_empty_config() -> None:
    """Test extracting figment names from an empty configuration."""
    figments = get_figments({})
    assert len(figments) == 0


@pytest.fixture
def figment_dir() -> Generator[Path, None, None]:
    """Create a temporary directory with figment configurations."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create a figment directory
        figment_path = temp_path / "test-figment"
        figment_path.mkdir()

        # Create a figment.yaml file
        with open(figment_path / "figment.yaml", "w") as f:
            yaml.dump({"name": "test-figment", "version": "1.0.0"}, f)

        yield temp_path


def test_get_figment_config(figment_dir: Path) -> None:
    """Test loading a figment configuration."""
    config = get_figment_config("test-figment", figment_dir)
    assert config["name"] == "test-figment"
    assert config["version"] == "1.0.0"


def test_get_figment_config_not_found(figment_dir: Path) -> None:
    """Test loading a non-existent figment configuration."""
    with pytest.raises(FileNotFoundError):
        get_figment_config("non-existent-figment", figment_dir)


def test_process_template_values_input() -> None:
    """Test processing template values with $INPUT."""
    config = {"key": "{{ $INPUT.value }}"}
    processed = process_template_values(config, "test-figment")
    assert processed["key"] == "{{ __test_figment__input__value }}"


def test_process_template_values_var() -> None:
    """Test processing template values with $VAR."""
    config = {"key": "{{ $VAR.value }}"}
    processed = process_template_values(config, "test-figment")
    assert processed["key"] == "{{ __test_figment__var__value }}"


def test_process_template_values_nested() -> None:
    """Test processing template values in nested structures."""
    config = {
        "key1": "{{ $INPUT.value1 }}",
        "key2": [
            "{{ $VAR.value2 }}",
            {"key3": "{{ $INPUT.value3 }}"}
        ]
    }
    processed = process_template_values(config, "test-figment")
    assert processed["key1"] == "{{ __test_figment__input__value1 }}"
    assert processed["key2"][0] == "{{ __test_figment__var__value2 }}"
    assert processed["key2"][1]["key3"] == "{{ __test_figment__input__value3 }}"


def test_process_template_values_invalid() -> None:
    """Test processing template values with invalid prefix."""
    config = {"key": "{{ $INVALID.value }}"}
    with pytest.raises(ValueError) as excinfo:
        process_template_values(config, "test-figment")
    assert "Invalid template variable" in str(excinfo.value)
    assert "Only '$INPUT.' and '$VAR.' prefixes are allowed" in str(excinfo.value)


def test_process_template_values_edge_cases() -> None:
    """Test processing template values with edge cases."""
    # Test with spaces in the template
    config1 = {"key": "{{ $INPUT.value }}"}
    processed1 = process_template_values(config1, "test-figment")
    assert processed1["key"] == "{{ __test_figment__input__value }}"

    # Test with multiple template variables in a single string
    config2 = {"key": "prefix {{ $INPUT.value1 }} middle {{ $VAR.value2 }} suffix"}
    processed2 = process_template_values(config2, "test-figment")
    expected = (
        "prefix {{ __test_figment__input__value1 }} "
        "middle {{ __test_figment__var__value2 }} suffix"
    )
    assert processed2["key"] == expected

    # Test with dots in the variable name
    config3 = {"key": "{{ $INPUT.nested.value }}"}
    processed3 = process_template_values(config3, "test-figment")
    assert processed3["key"] == "{{ __test_figment__input__nested.value }}"

    # Test with hyphens in the figment name
    config4 = {"key": "{{ $INPUT.value }}"}
    processed4 = process_template_values(config4, "test-with-hyphens")
    assert processed4["key"] == "{{ __test_with_hyphens__input__value }}"

    # Test with non-$ values
    config5 = {"key": "{{ some_value }}"}
    with pytest.raises(ValueError) as excinfo:
        process_template_values(config5, "test-figment")
    assert "Invalid template variable" in str(excinfo.value)
    assert "Only '$INPUT.' and '$VAR.' prefixes are allowed" in str(excinfo.value)

    # Test with mixed $ and non-$ values
    config6 = {"key": "prefix {{ some_value }} middle {{ $INPUT.value }} suffix"}
    with pytest.raises(ValueError) as excinfo:
        process_template_values(config6, "test-figment")
    assert "Invalid template variable" in str(excinfo.value)
    assert "Only '$INPUT.' and '$VAR.' prefixes are allowed" in str(excinfo.value)
