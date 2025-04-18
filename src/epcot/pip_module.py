"""Pip module for EPCOT.

This module provides the PipModule class for figment pip modules.
"""

from typing import Dict, Any


class PipModule:
    """Pip module configuration for a figment."""

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize a pip module.

        Args:
            config: Configuration for the pip module.
        """
        self.config = config
