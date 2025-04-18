"""
Handler module for the Ansible Development Kit (ADK).

This module provides the Handler class for representing Ansible handlers.
"""

from typing import Dict, List, Optional, Any
from .task import Task

class Handler(Task):
    """
    Represents an Ansible handler.

    A handler is a task that is triggered by a notify action from another task.
    """

    def __init__(
        self,
        name: str,
        module: str,
        args: Dict[str, Any],
        when: Optional[str] = None,
        register: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> None:
        """
        Initialize a Handler.

        Args:
            name: The name of the handler
            module: The Ansible module to use
            args: Arguments to pass to the module
            when: Conditional expression for when to run the handler
            register: Variable name to store the result
            tags: List of tags to apply to the handler
        """
        super().__init__(name, module, args, when, register, tags)