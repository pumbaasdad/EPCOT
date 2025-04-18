"""
Tests for the Config module.
"""

import os
import pytest
import tempfile
import yaml
from epcot.config import Config


@pytest.fixture
def sample_config_file():
    """Create a temporary config file for testing."""
    config_data = {
        "ansible": {
            "inventory": "/path/to/inventory.yml",
            "private_key": "/path/to/private_key",
        },
        "figments": {
            "directory": "/path/to/figments",
        },
        "logging": {
            "level": "INFO",
            "file": "/path/to/epcot.log",
        },
    }
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(config_data, f)
        config_file = f.name
    
    yield config_file
    
    # Cleanup
    os.unlink(config_file)


def test_config_creation():
    """Test that a Config can be created with the correct attributes."""
    config = Config(
        ansible={"inventory": "/path/to/inventory.yml"},
        figments={"directory": "/path/to/figments"},
        logging={"level": "INFO"},
    )
    
    assert config.ansible == {"inventory": "/path/to/inventory.yml"}
    assert config.figments == {"directory": "/path/to/figments"}
    assert config.logging == {"level": "INFO"}


def test_config_creation_defaults():
    """Test that a Config can be created with default values."""
    config = Config()
    
    assert config.ansible == {}
    assert config.figments == {}
    assert config.logging == {}


def test_config_from_file(sample_config_file):
    """Test that a Config can be loaded from a file."""
    config = Config.from_file(sample_config_file)
    
    assert config.ansible == {
        "inventory": "/path/to/inventory.yml",
        "private_key": "/path/to/private_key",
    }
    assert config.figments == {
        "directory": "/path/to/figments",
    }
    assert config.logging == {
        "level": "INFO",
        "file": "/path/to/epcot.log",
    }


def test_config_from_file_not_found():
    """Test that loading a Config from a non-existent file raises an error."""
    with pytest.raises(FileNotFoundError):
        Config.from_file("/path/to/nonexistent/file.yaml")


def test_get_ansible_config():
    """Test that get_ansible_config returns the correct configuration."""
    config = Config(
        ansible={"inventory": "/path/to/inventory.yml"},
    )
    
    assert config.get_ansible_config() == {"inventory": "/path/to/inventory.yml"}


def test_get_figments_config():
    """Test that get_figments_config returns the correct configuration."""
    config = Config(
        figments={"directory": "/path/to/figments"},
    )
    
    assert config.get_figments_config() == {"directory": "/path/to/figments"}


def test_get_logging_config():
    """Test that get_logging_config returns the correct configuration."""
    config = Config(
        logging={"level": "INFO"},
    )
    
    assert config.get_logging_config() == {"level": "INFO"}