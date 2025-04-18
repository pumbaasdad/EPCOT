"""Service module for EPCOT.

This module provides the Service class for figment services.
"""

from typing import Dict, Any


class Service:
    """Service configuration for a figment."""

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize a service.

        Args:
            config: Configuration for the service.
        """
        self.config = config