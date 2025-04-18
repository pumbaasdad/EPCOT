"""Configuration module for EPCOT.

This module provides utilities for loading and parsing EPCOT configuration files.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, cast
import yaml


def load_config(config_path: Path) -> Dict[str, Any]:
    """Load an EPCOT configuration file.

    Args:
        config_path: Path to the configuration file.

    Returns:
        The parsed configuration as a dictionary.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        yaml.YAMLError: If the configuration file is not valid YAML.
    """
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, "r") as f:
        return cast(Dict[str, Any], yaml.safe_load(f))


def get_figments(config: Dict[str, Any]) -> List[str]:
    """Extract the list of figments from an EPCOT configuration.

    Args:
        config: The parsed EPCOT configuration.

    Returns:
        A list of figment names.
    """
    figments: List[str] = []

    if "figments" in config:
        for item in config["figments"]:
            if isinstance(item, str):
                figments.append(item)
            elif isinstance(item, dict):
                figments.extend(item.keys())

    return figments


def get_figment_config(
    figment_name: str, config_dir: Optional[Path] = None
) -> Dict[str, Any]:
    """Load the configuration for a specific figment.

    Args:
        figment_name: The name of the figment.
        config_dir: The directory containing figment configurations.
            Defaults to the current directory.

    Returns:
        The parsed figment configuration.

    Raises:
        FileNotFoundError: If the figment configuration file does not exist.
    """
    if config_dir is None:
        config_dir = Path(".")

    figment_path = config_dir / figment_name / "figment.yaml"

    return load_config(figment_path)
