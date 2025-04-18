"""Figment module for EPCOT.

This module provides the Figment abstract base class that all figments must inherit
from.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class Figment(ABC):
    """Abstract base class for all figments.

    All figments must inherit from this class and implement its abstract methods.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize a figment.

        Args:
            config: Optional configuration for the figment.
        """
        self.config = config or {}

    @abstractmethod
    def run(self) -> None:
        """Run the figment.

        This method must be implemented by all figments.
        """
        pass
