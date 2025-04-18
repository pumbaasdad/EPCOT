"""CLI module for EPCOT.

This module provides the command-line interface for EPCOT.
"""

import importlib
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Union, cast

from epcot.config import load_config
from epcot.figment import Figment


def validate_figments_list(figments: Any) -> List[Union[str, Dict[str, Any]]]:
    """Validate that figments is a list of strings or single-key dictionaries.

    Args:
        figments: The value of the figments key from the config.

    Returns:
        The validated list of figments.

    Raises:
        ValueError: If figments is not a list or contains invalid entries.
    """
    if not isinstance(figments, list):
        raise ValueError("figments must be a list")

    for item in figments:
        if not isinstance(item, (str, dict)):
            raise ValueError(
                f"figment must be a string or dictionary, got {type(item).__name__}"
            )
        if isinstance(item, dict) and len(item) != 1:
            raise ValueError(
                f"figment dictionary must have exactly one key, got {len(item)}"
            )

    return figments


def validate_figment_name(name: str) -> str:
    """Validate that a figment name is in kabab-case.

    Args:
        name: The figment name to validate.

    Returns:
        The validated figment name.

    Raises:
        ValueError: If the figment name is not in kabab-case.
    """
    if not re.match(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$", name):
        raise ValueError(f"figment name must be in kabab-case: {name}")
    return name


def to_pascal_case(name: str) -> str:
    """Convert a kabab-case string to PascalCase.

    Args:
        name: The kabab-case string to convert.

    Returns:
        The PascalCase string.
    """
    return "".join(word.capitalize() for word in name.split("-"))


def get_figment_class(name: str) -> type:
    """Get the figment class for a given name.

    Args:
        name: The figment name in kabab-case.

    Returns:
        The figment class.

    Raises:
        ImportError: If the figment module cannot be imported.
        AttributeError: If the figment class cannot be found.
        TypeError: If the figment class does not inherit from Figment.
    """
    pascal_name = to_pascal_case(name)

    try:
        module = importlib.import_module(f"epcot.figments.{name}")
    except ImportError:
        raise ImportError(f"Could not import figment module: epcot.figments.{name}")

    try:
        figment_class = getattr(module, pascal_name)
    except AttributeError:
        raise AttributeError(f"Could not find figment class: {pascal_name}")

    if not isinstance(figment_class, type):
        raise TypeError(f"Figment class must be a class: {pascal_name}")

    if not issubclass(figment_class, Figment):
        raise TypeError(f"Figment class must inherit from Figment: {pascal_name}")

    return figment_class


def main() -> int:
    """Main entry point for the EPCOT CLI.

    Returns:
        Exit code.
    """
    try:
        config_path = Path("epcot.yaml")
        config = load_config(config_path)

        if "figments" not in config:
            print("No figments found in configuration")
            return 1

        figments_list = validate_figments_list(config["figments"])

        for item in figments_list:
            if isinstance(item, str):
                name = validate_figment_name(item)
                figment_config = {}
            else:
                name = validate_figment_name(list(item.keys())[0])
                figment_config = cast(Dict[str, Any], item[name])

            figment_class = get_figment_class(name)
            _ = figment_class(figment_config)

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
