"""Task module for Ansible Development Kit (adk).

This module provides the Task abstract base class that all tasks must inherit
from.
"""

from abc import ABC
from typing import Dict, Any, Optional


class Task(ABC):
    """Abstract base class for all tasks.

    All tasks must inherit from this class. Abstract methods will be added later.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize a task.

        Args:
            config: Optional configuration for the task.
        """
        self.config = config or {}
