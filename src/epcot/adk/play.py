"""
Play module for the Ansible Development Kit (ADK).

This module provides the Play class for representing Ansible plays.
"""

from typing import Dict, List, Optional, Union, Any
from .task import Task
from .handler import Handler

class Play:
    """
    Represents a play in an Ansible playbook.

    A play is a set of tasks to be executed on a specific set of hosts.
    """

    def __init__(
        self,
        name: str,
        hosts: Union[str, List[str]],
        become: bool = False,
        vars: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize a Play.

        Args:
            name: The name of the play
            hosts: The hosts or host groups to run the play on
            become: Whether to use privilege escalation
            vars: Variables to use in the play
        """
        self.name = name
        self.hosts = hosts
        self.become = become
        self.vars = vars or {}
        self.tasks: List[Task] = []
        self.handlers: List[Handler] = []
        self.dependencies: Dict[str, List[str]] = {}  # task_name -> [dependency_task_names]

    def add_task(self, task: Task) -> None:
        """
        Add a task to the play.

        Args:
            task: The task to add
        """
        self.tasks.append(task)

    def add_handler(self, handler: Handler) -> None:
        """
        Add a handler to the play.

        Args:
            handler: The handler to add
        """
        self.handlers.append(handler)

    def add_dependency(self, task_name: str, depends_on: str) -> None:
        """
        Add a dependency between tasks.

        Args:
            task_name: The name of the task that depends on another task
            depends_on: The name of the task that must run before the dependent task
        """
        if task_name not in self.dependencies:
            self.dependencies[task_name] = []
        self.dependencies[task_name].append(depends_on)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the play to a dictionary representation.

        Returns:
            A dictionary representation of the play
        """
        play_dict = {
            "name": self.name,
            "hosts": self.hosts,
            "become": self.become,
            "vars": self.vars,
            "tasks": [self._task_to_dict(task) for task in self.tasks],
        }

        if self.handlers:
            play_dict["handlers"] = [self._task_to_dict(handler) for handler in self.handlers]

        return play_dict

    def _task_to_dict(self, task: Union[Task, Handler]) -> Dict[str, Any]:
        """
        Convert a task or handler to a dictionary representation.

        Args:
            task: The task or handler to convert

        Returns:
            A dictionary representation of the task or handler
        """
        task_dict = {
            "name": task.name,
            task.module: task.args,
        }

        if task.when:
            task_dict["when"] = task.when

        if task.register:
            task_dict["register"] = task.register

        if task.tags:
            task_dict["tags"] = task.tags

        return task_dict