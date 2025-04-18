"""Tests for the config module."""

import pytest
from pathlib import Path
import tempfile
import yaml
from typing import Dict, Any, Generator

from epcot.config import load_config, get_figments, get_figment_config


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
