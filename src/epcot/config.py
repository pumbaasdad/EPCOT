"""Configuration module for EPCOT.

This module provides utilities for loading and parsing EPCOT configuration files.
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, cast
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


def process_template_values(
    config: Union[Dict[str, Any], List[Any], str, Any], figment_name: str
) -> Union[Dict[str, Any], List[Any], str, Any]:
    """Process template values in the configuration.

    Recursively checks all values in the configuration. If a value is a string
    containing "{{ }}", it processes it as follows:
    - If it begins with "$INPUT.", it replaces it with "__<figment_name>__input__...".
    - If it begins with "$VAR.", it replaces it with "__<figment_name>__var__...".
    - If it begins with any other prefix, it raises an error.

    Args:
        config: The configuration to process.
        figment_name: The name of the figment.

    Returns:
        The processed configuration.

    Raises:
        ValueError: If a template value doesn't begin with "$INPUT." or "$VAR.".
    """
    # Replace hyphens with underscores in figment name
    safe_figment_name = figment_name.replace("-", "_")

    # Regular expression to match any value within {{ }}
    template_pattern = re.compile(r"\{\{\s*([A-Za-z0-9_.$-]+)\s*\}\}")

    if isinstance(config, dict):
        # Process dictionary values
        return {k: process_template_values(v, figment_name) for k, v in config.items()}
    elif isinstance(config, list):
        # Process list values
        return [process_template_values(item, figment_name) for item in config]
    elif isinstance(config, str):
        # Process string values
        def replace_template(match):
            template_var = match.group(1)
            if template_var.startswith("$INPUT."):
                # Replace $INPUT. with __<figment name>__input__
                return (
                    "{{ __" + safe_figment_name + "__input__" + template_var[7:] + " }}"
                )
            elif template_var.startswith("$VAR."):
                # Replace $VAR. with __<figment name>__var__
                return (
                    "{{ __" + safe_figment_name + "__var__" + template_var[5:] + " }}"
                )
            else:
                # Raise error for any other template variables
                raise ValueError(
                    f"Invalid template variable '{template_var}' "
                    f"in figment '{figment_name}'. "
                    f"Only '$INPUT.' and '$VAR.' prefixes are allowed."
                )

        # Find all template variables and process them
        matches = template_pattern.findall(config)
        if matches:
            return template_pattern.sub(replace_template, config)
        return config
    else:
        # Return other values as-is
        return config


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
        ValueError: If a template value doesn't begin with "$INPUT." or "$VAR.".
    """
    if config_dir is None:
        config_dir = Path(".")

    figment_path = config_dir / figment_name / "figment.yaml"

    # Load the configuration
    config = load_config(figment_path)

    # Process template values
    return process_template_values(config, figment_name)
