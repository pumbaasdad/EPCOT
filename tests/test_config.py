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


def test_load_config_has_figments(config_file: Path) -> None:
    """Test loading a configuration file has figments key."""
    config = load_config(config_file)
    assert "figments" in config


def test_load_config_figments_count(config_file: Path) -> None:
    """Test loading a configuration file has correct number of figments."""
    config = load_config(config_file)
    assert len(config["figments"]) == 5


def test_load_config_file_not_found() -> None:
    """Test loading a non-existent configuration file."""
    with pytest.raises(FileNotFoundError):
        load_config(Path("non_existent_file.yaml"))


def test_get_figments_count(sample_config: Dict[str, Any]) -> None:
    """Test extracting figment names count from a configuration."""
    figments = get_figments(sample_config)
    assert len(figments) == 5


def test_get_figments_contains_backup(sample_config: Dict[str, Any]) -> None:
    """Test figments contains backup."""
    figments = get_figments(sample_config)
    assert "backup" in figments


def test_get_figments_contains_certificates(sample_config: Dict[str, Any]) -> None:
    """Test figments contains certificates."""
    figments = get_figments(sample_config)
    assert "certificates" in figments


def test_get_figments_contains_dhcp(sample_config: Dict[str, Any]) -> None:
    """Test figments contains dhcp."""
    figments = get_figments(sample_config)
    assert "dhcp" in figments


def test_get_figments_contains_reverse_proxy(sample_config: Dict[str, Any]) -> None:
    """Test figments contains reverse-proxy."""
    figments = get_figments(sample_config)
    assert "reverse-proxy" in figments


def test_get_figments_contains_transcode(sample_config: Dict[str, Any]) -> None:
    """Test figments contains transcode."""
    figments = get_figments(sample_config)
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


def test_get_figment_config_name(figment_dir: Path) -> None:
    """Test loading a figment configuration has correct name."""
    config = get_figment_config("test-figment", figment_dir)
    assert config["name"] == "test-figment"


def test_get_figment_config_version(figment_dir: Path) -> None:
    """Test loading a figment configuration has correct version."""
    config = get_figment_config("test-figment", figment_dir)
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


def test_process_template_values_nested_top_level() -> None:
    """Test processing template values in top level of nested structures."""
    config = {
        "key1": "{{ $INPUT.value1 }}",
        "key2": [
            "{{ $VAR.value2 }}",
            {"key3": "{{ $INPUT.value3 }}"}
        ]
    }
    processed = process_template_values(config, "test-figment")
    assert processed["key1"] == "{{ __test_figment__input__value1 }}"


def test_process_template_values_nested_list_item() -> None:
    """Test processing template values in list item of nested structures."""
    config = {
        "key1": "{{ $INPUT.value1 }}",
        "key2": [
            "{{ $VAR.value2 }}",
            {"key3": "{{ $INPUT.value3 }}"}
        ]
    }
    processed = process_template_values(config, "test-figment")
    assert processed["key2"][0] == "{{ __test_figment__var__value2 }}"


def test_process_template_values_nested_dict_in_list() -> None:
    """Test processing template values in dictionary inside list of nested structures."""
    config = {
        "key1": "{{ $INPUT.value1 }}",
        "key2": [
            "{{ $VAR.value2 }}",
            {"key3": "{{ $INPUT.value3 }}"}
        ]
    }
    processed = process_template_values(config, "test-figment")
    assert processed["key2"][1]["key3"] == "{{ __test_figment__input__value3 }}"


def test_process_template_values_invalid() -> None:
    """Test processing template values with invalid prefix."""
    config = {"key": "{{ $INVALID.value }}"}
    with pytest.raises(ValueError) as excinfo:
        process_template_values(config, "test-figment")
    assert "Invalid template variable" in str(excinfo.value)
    assert "Only '$INPUT.' and '$VAR.' prefixes are allowed" in str(excinfo.value)


def test_process_template_values_with_spaces() -> None:
    """Test processing template values with spaces in the template."""
    config = {"key": "{{ $INPUT.value }}"}
    processed = process_template_values(config, "test-figment")
    assert processed["key"] == "{{ __test_figment__input__value }}"


def test_process_template_values_multiple_variables() -> None:
    """Test processing multiple template variables in a single string."""
    config = {"key": "prefix {{ $INPUT.value1 }} middle {{ $VAR.value2 }} suffix"}
    processed = process_template_values(config, "test-figment")
    expected = (
        "prefix {{ __test_figment__input__value1 }} "
        "middle {{ __test_figment__var__value2 }} suffix"
    )
    assert processed["key"] == expected


def test_process_template_values_with_dots() -> None:
    """Test processing template values with dots in the variable name."""
    config = {"key": "{{ $INPUT.nested.value }}"}
    processed = process_template_values(config, "test-figment")
    assert processed["key"] == "{{ __test_figment__input__nested.value }}"


def test_process_template_values_with_hyphens_in_figment() -> None:
    """Test processing template values with hyphens in the figment name."""
    config = {"key": "{{ $INPUT.value }}"}
    processed = process_template_values(config, "test-with-hyphens")
    assert processed["key"] == "{{ __test_with_hyphens__input__value }}"


def test_process_template_values_with_non_dollar_values() -> None:
    """Test processing template values with non-$ values."""
    config = {"key": "{{ some_value }}"}
    with pytest.raises(ValueError) as excinfo:
        process_template_values(config, "test-figment")
    assert "Invalid template variable" in str(excinfo.value)
    assert "Only '$INPUT.' and '$VAR.' prefixes are allowed" in str(excinfo.value)


def test_process_template_values_with_mixed_values() -> None:
    """Test processing template values with mixed $ and non-$ values."""
    config = {"key": "prefix {{ some_value }} middle {{ $INPUT.value }} suffix"}
    with pytest.raises(ValueError) as excinfo:
        process_template_values(config, "test-figment")
    assert "Invalid template variable" in str(excinfo.value)
    assert "Only '$INPUT.' and '$VAR.' prefixes are allowed" in str(excinfo.value)
