"""Directory module for EPCOT.

This module provides the Directory class for figment directories.
"""

from typing import Dict, Any


class Directory:
    """Directory configuration for a figment."""

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize a directory.

        Args:
            config: Configuration for the directory.
        """
        self.config = config
