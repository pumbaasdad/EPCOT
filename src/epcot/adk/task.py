"""
Task module for the Ansible Development Kit (ADK).

This module provides the Task class for representing Ansible tasks.
"""

from typing import Dict, List, Optional, Any
import yaml

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

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the task to a dictionary representation.

        Returns:
            A dictionary representation of the task
        """
        task_dict = {
            "name": self.name,
            self.module: self.args,
        }

        if self.when:
            task_dict["when"] = self.when

        if self.register:
            task_dict["register"] = self.register

        if self.tags:
            task_dict["tags"] = self.tags

        return task_dict

    def to_yaml(self) -> str:
        """
        Convert the task to a YAML string.

        Returns:
            A YAML string representation of the task

        Raises:
            yaml.YAMLError: If the task cannot be converted to YAML
        """
        task_dict = self.to_dict()
        try:
            return yaml.dump([task_dict], default_flow_style=False)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Failed to convert task '{self.name}' to YAML: {e}")

    def to_runner_dict(self) -> Dict[str, Any]:
        """
        Convert the task to a dictionary representation for ansible_runner.

        Returns:
            A dictionary representation of the task suitable for ansible_runner

        Note:
            This is similar to to_dict() but may include additional fields
            required by ansible_runner.
        """
        # For a single task, the runner dict is the same as the regular dict
        return self.to_dict()

    def validate_runner(self) -> List[str]:
        """
        Validate the task for ansible_runner conversion.

        Returns:
            A list of validation errors, or an empty list if the task is valid for ansible_runner
        """
        # Basic validation is the same as for regular validation
        return self.validate()

    def is_valid_runner(self) -> bool:
        """
        Check if the task is valid for ansible_runner conversion.

        Returns:
            True if the task is valid for ansible_runner, False otherwise
        """
        return len(self.validate_runner()) == 0

    def validate(self) -> List[str]:
        """
        Validate the task.

        Returns:
            A list of validation errors, or an empty list if the task is valid
        """
        errors = []

        if not self.name:
            errors.append("Task must have a name")

        if not self.module:
            errors.append("Task must have a module")

        if not isinstance(self.args, dict):
            errors.append("Task arguments must be a dictionary")

        return errors

    def is_valid(self) -> bool:
        """
        Check if the task is valid.

        Returns:
            True if the task is valid, False otherwise
        """
        return len(self.validate()) == 0