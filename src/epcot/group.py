"""Group module for EPCOT.

This module provides the Group class for figment groups.
"""

from typing import Dict, Any


class Group:
    """Group configuration for a figment."""

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize a group.

        Args:
            config: Configuration for the group.
        """
        self.config = config