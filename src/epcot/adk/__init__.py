"""
Ansible Development Kit (ADK) module.

This module provides a programmatic interface for creating and managing Ansible tasks and playbooks.
"""

from typing import Dict, List, Optional, Union, Any

__all__ = ["Task", "Playbook", "TaskResult"]


class Task:
    """
    Represents an Ansible task.
    
    A task is a single action to be performed on a host.
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
        Initialize a Task.
        
        Args:
            name: The name of the task
            module: The Ansible module to use
            args: Arguments to pass to the module
            when: Conditional expression for when to run the task
            register: Variable name to store the result
            tags: List of tags to apply to the task
        """
        self.name = name
        self.module = module
        self.args = args
        self.when = when
        self.register = register
        self.tags = tags or []


class Playbook:
    """
    Represents an Ansible playbook.
    
    A playbook is a collection of tasks to be executed on specified hosts.
    """
    
    def __init__(
        self,
        name: str,
        hosts: Union[str, List[str]],
        become: bool = False,
        vars: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize a Playbook.
        
        Args:
            name: The name of the playbook
            hosts: The hosts or host groups to run the playbook on
            become: Whether to use privilege escalation
            vars: Variables to use in the playbook
        """
        self.name = name
        self.hosts = hosts
        self.become = become
        self.vars = vars or {}
        self.tasks: List[Task] = []
    
    def add_task(self, task: Task) -> None:
        """
        Add a task to the playbook.
        
        Args:
            task: The task to add
        """
        self.tasks.append(task)
    
    def run(self) -> "TaskResult":
        """
        Run the playbook.
        
        Returns:
            The result of running the playbook
        """
        # This would be implemented to actually run the playbook
        return TaskResult(success=True)


class TaskResult:
    """
    Represents the result of running a task or playbook.
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
            success: Whether the task was successful
            changed: Whether the task changed the system
            error: Error message if the task failed
            output: Output from the task
        """
        self.success = success
        self.changed = changed
        self.error = error
        self.output = output or {}