"""
TaskResult module for the Ansible Development Kit (ADK).

This module provides the TaskResult class for representing the result of running an Ansible task or playbook.
"""

from typing import Dict, Optional, Any

class TaskResult:
    """
    Represents the result of running an Ansible task or playbook.
    """
    
    def __init__(
        self,
        success: bool,
        changed: bool = False,
        error: Optional[str] = None,
        output: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize a TaskResult.
        
        Args:
            success: Whether the task or playbook was successful
            changed: Whether the task or playbook changed the system
            error: Error message if the task or playbook failed
            output: Output from the task or playbook
        """
        self.success = success
        self.changed = changed
        self.error = error
        self.output = output or {}