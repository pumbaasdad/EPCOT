"""
Ansible Development Kit (ADK) module.

This module provides a programmatic interface for creating and managing Ansible tasks and playbooks.
"""

from typing import Dict, List, Optional, Union, Any, Set, TextIO, BinaryIO, Callable
from collections import defaultdict
import os
import yaml
import tempfile
import ansible_runner
from pathlib import Path

__all__ = [
    "Task", "Play", "Playbook", "TaskResult", "Handler", 
    "to_yaml", "to_yaml_file", "run_playbook", "run_playbook_with_runner"
]


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


class Playbook:
    """
    Represents an Ansible playbook.

    A playbook is a collection of plays, each containing tasks to be executed on specified hosts.
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
        self.plays: List[Play] = []
        self.handlers: List[Handler] = []
        self._default_play: Optional[Play] = None
        self._task_dependencies: Dict[str, List[str]] = {}  # task_name -> [dependency_task_names]

    @property
    def default_play(self) -> Play:
        """
        Get the default play for the playbook.

        If no plays have been explicitly created, a default play is created.

        Returns:
            The default play
        """
        if not self._default_play:
            self._default_play = Play(
                name=self.name,
                hosts=self.hosts,
                become=self.become,
                vars=self.vars,
            )
            self.plays.append(self._default_play)
        return self._default_play

    @property
    def tasks(self) -> List[Task]:
        """
        Get all tasks from all plays in the playbook.

        Returns:
            A list of all tasks
        """
        all_tasks = []
        for play in self.plays:
            all_tasks.extend(play.tasks)
        return all_tasks

    def add_play(self, play: Play) -> None:
        """
        Add a play to the playbook.

        Args:
            play: The play to add
        """
        self.plays.append(play)

    def create_play(
        self,
        name: str,
        hosts: Optional[Union[str, List[str]]] = None,
        become: Optional[bool] = None,
        vars: Optional[Dict[str, Any]] = None,
    ) -> Play:
        """
        Create a new play and add it to the playbook.

        Args:
            name: The name of the play
            hosts: The hosts or host groups to run the play on (defaults to playbook hosts)
            become: Whether to use privilege escalation (defaults to playbook become)
            vars: Variables to use in the play (defaults to playbook vars)

        Returns:
            The created play
        """
        play = Play(
            name=name,
            hosts=hosts if hosts is not None else self.hosts,
            become=become if become is not None else self.become,
            vars=vars if vars is not None else dict(self.vars),
        )
        self.add_play(play)
        return play

    def add_task(self, task: Task, play: Optional[Play] = None) -> None:
        """
        Add a task to the playbook.

        If no play is specified, the task is added to the default play.

        Args:
            task: The task to add
            play: The play to add the task to (defaults to the default play)
        """
        if play:
            play.add_task(task)
        else:
            self.default_play.add_task(task)

    def add_handler(self, handler: Handler, play: Optional[Play] = None) -> None:
        """
        Add a handler to the playbook.

        If no play is specified, the handler is added to the playbook-level handlers.

        Args:
            handler: The handler to add
            play: The play to add the handler to (defaults to playbook-level handlers)
        """
        if play:
            play.add_handler(handler)
        else:
            self.handlers.append(handler)

    def add_dependency(self, task_name: str, depends_on: str, play: Optional[Play] = None) -> None:
        """
        Add a dependency between tasks.

        If no play is specified, the dependency is added to the playbook-level dependencies.

        Args:
            task_name: The name of the task that depends on another task
            depends_on: The name of the task that must run before the dependent task
            play: The play to add the dependency to (defaults to playbook-level dependencies)
        """
        if play:
            play.add_dependency(task_name, depends_on)
        else:
            if task_name not in self._task_dependencies:
                self._task_dependencies[task_name] = []
            self._task_dependencies[task_name].append(depends_on)

    def set_vars(self, vars: Dict[str, Any]) -> None:
        """
        Set variables for the playbook.

        Args:
            vars: The variables to set
        """
        self.vars.update(vars)

    def validate(self) -> List[str]:
        """
        Validate the playbook.

        Returns:
            A list of validation errors, or an empty list if the playbook is valid
        """
        errors = []

        # Check that we have at least one play
        if not self.plays:
            errors.append("Playbook must have at least one play")

        # Check that all plays have hosts
        for i, play in enumerate(self.plays):
            if not play.hosts:
                errors.append(f"Play {i} ({play.name}) must have hosts")

        # Check that all task names are unique
        task_names = set()
        for play in self.plays:
            for task in play.tasks:
                if task.name in task_names:
                    errors.append(f"Duplicate task name: {task.name}")
                task_names.add(task.name)

        # Check that all handler names are unique
        handler_names = set()
        for handler in self.handlers:
            if handler.name in handler_names:
                errors.append(f"Duplicate handler name: {handler.name}")
            handler_names.add(handler.name)

        for play in self.plays:
            for handler in play.handlers:
                if handler.name in handler_names:
                    errors.append(f"Duplicate handler name: {handler.name}")
                handler_names.add(handler.name)

        # Check that all dependencies refer to existing tasks
        for task_name, dependencies in self._task_dependencies.items():
            if task_name not in task_names:
                errors.append(f"Dependency refers to non-existent task: {task_name}")
            for dependency in dependencies:
                if dependency not in task_names:
                    errors.append(f"Dependency refers to non-existent task: {dependency}")

        for play in self.plays:
            for task_name, dependencies in play.dependencies.items():
                if task_name not in task_names:
                    errors.append(f"Dependency refers to non-existent task: {task_name}")
                for dependency in dependencies:
                    if dependency not in task_names:
                        errors.append(f"Dependency refers to non-existent task: {dependency}")

        return errors

    def is_valid(self) -> bool:
        """
        Check if the playbook is valid.

        Returns:
            True if the playbook is valid, False otherwise
        """
        return len(self.validate()) == 0

    def order_tasks(self) -> None:
        """
        Order tasks based on dependencies.

        This method reorders the tasks in each play based on the dependencies between tasks.
        Tasks with no dependencies are placed first, followed by tasks that depend on them, and so on.
        """
        for play in self.plays:
            # Collect all task names and their dependencies
            task_deps = defaultdict(set)
            for task in play.tasks:
                task_deps[task.name] = set()

            # Add play-level dependencies
            for task_name, dependencies in play.dependencies.items():
                for dependency in dependencies:
                    task_deps[task_name].add(dependency)

            # Add playbook-level dependencies
            for task_name, dependencies in self._task_dependencies.items():
                for dependency in dependencies:
                    if task_name in task_deps:
                        task_deps[task_name].add(dependency)

            # Topological sort
            ordered_tasks = []
            visited = set()
            temp_visited = set()

            def visit(task_name):
                if task_name in temp_visited:
                    # Cyclic dependency
                    return
                if task_name in visited:
                    return

                temp_visited.add(task_name)

                for dependency in task_deps[task_name]:
                    visit(dependency)

                temp_visited.remove(task_name)
                visited.add(task_name)
                ordered_tasks.append(task_name)

            for task_name in task_deps:
                if task_name not in visited:
                    visit(task_name)

            # Reorder tasks based on the topological sort
            task_map = {task.name: task for task in play.tasks}
            play.tasks = [task_map[name] for name in ordered_tasks if name in task_map]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the playbook to a dictionary representation.

        Returns:
            A dictionary representation of the playbook
        """
        # Order tasks based on dependencies
        self.order_tasks()

        # Convert plays to dictionaries
        plays = [play.to_dict() for play in self.plays]

        # Add playbook-level handlers if any
        if self.handlers:
            for play in plays:
                if "handlers" not in play:
                    play["handlers"] = []
                play["handlers"].extend([
                    {
                        "name": handler.name,
                        handler.module: handler.args,
                        **({"when": handler.when} if handler.when else {}),
                        **({"register": handler.register} if handler.register else {}),
                        **({"tags": handler.tags} if handler.tags else {}),
                    }
                    for handler in self.handlers
                ])

        return plays

    def run(self) -> "TaskResult":
        """
        Run the playbook.

        Returns:
            The result of running the playbook
        """
        # This would be implemented to actually run the playbook
        return TaskResult(success=True)

    def to_yaml(self) -> str:
        """
        Convert the playbook to a YAML string.

        Returns:
            A YAML string representation of the playbook

        Raises:
            yaml.YAMLError: If the playbook cannot be converted to YAML
        """
        playbook_dict = self.to_dict()
        try:
            return yaml.dump(playbook_dict, default_flow_style=False)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Failed to convert playbook '{self.name}' to YAML: {e}")

    def to_runner_dict(self) -> Dict[str, Any]:
        """
        Convert the playbook to a dictionary representation for ansible_runner.

        Returns:
            A dictionary representation of the playbook suitable for ansible_runner

        Note:
            This creates a dictionary structure that can be used with ansible_runner.run()
        """
        # Order tasks based on dependencies
        self.order_tasks()

        # Convert plays to dictionaries
        playbook_dict = self.to_dict()

        # ansible_runner expects a dictionary with specific keys
        runner_dict = {
            "playbook": playbook_dict
        }

        return runner_dict

    def validate_runner(self) -> List[str]:
        """
        Validate the playbook for ansible_runner conversion.

        Returns:
            A list of validation errors, or an empty list if the playbook is valid for ansible_runner
        """
        errors = self.validate()

        # Additional validation for ansible_runner
        for play in self.plays:
            for task in play.tasks:
                task_errors = task.validate_runner()
                if task_errors:
                    errors.append(f"Task '{task.name}' is invalid for ansible_runner: {', '.join(task_errors)}")

            for handler in play.handlers:
                handler_errors = handler.validate_runner()
                if handler_errors:
                    errors.append(f"Handler '{handler.name}' is invalid for ansible_runner: {', '.join(handler_errors)}")

        for handler in self.handlers:
            handler_errors = handler.validate_runner()
            if handler_errors:
                errors.append(f"Handler '{handler.name}' is invalid for ansible_runner: {', '.join(handler_errors)}")

        return errors

    def is_valid_runner(self) -> bool:
        """
        Check if the playbook is valid for ansible_runner conversion.

        Returns:
            True if the playbook is valid for ansible_runner, False otherwise
        """
        return len(self.validate_runner()) == 0

    def run_with_runner(
        self, 
        inventory: Optional[Union[str, Dict[str, Any]]] = None,
        private_data_dir: Optional[str] = None,
        **kwargs: Any
    ) -> "TaskResult":
        """
        Run the playbook using ansible_runner.

        Args:
            inventory: The inventory to use (path to inventory file or inventory dict)
            private_data_dir: The private data directory to use
            **kwargs: Additional arguments to pass to ansible_runner.run()

        Returns:
            The result of running the playbook

        Raises:
            ValueError: If the playbook is invalid for ansible_runner
        """
        if not self.is_valid_runner():
            errors = self.validate_runner()
            raise ValueError(f"Playbook is invalid for ansible_runner: {', '.join(errors)}")

        # Create a temporary directory for the playbook if no private_data_dir is provided
        temp_dir = None
        if not private_data_dir:
            temp_dir = tempfile.TemporaryDirectory()
            private_data_dir = temp_dir.name

        try:
            # Convert the playbook to a dictionary for ansible_runner
            playbook_dict = self.to_runner_dict()

            # Set up the inventory
            if inventory:
                if isinstance(inventory, dict):
                    # Create inventory file in the private data dir
                    os.makedirs(os.path.join(private_data_dir, "inventory"), exist_ok=True)
                    with open(os.path.join(private_data_dir, "inventory", "hosts"), "w") as f:
                        yaml.dump(inventory, f)
                else:
                    # Use the provided inventory file
                    playbook_dict["inventory"] = inventory

            # Run the playbook
            result = ansible_runner.run(
                private_data_dir=private_data_dir,
                playbook=playbook_dict["playbook"],
                **kwargs
            )

            # Convert the result to a TaskResult
            return TaskResult(
                success=(result.rc == 0),
                changed=any(event.get("event_data", {}).get("changed", False) 
                           for event in result.events if event.get("event") == "runner_on_ok"),
                error=result.stderr if result.rc != 0 else None,
                output={
                    "rc": result.rc,
                    "status": result.status,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "events": [event for event in result.events],
                    "stats": result.stats
                }
            )
        finally:
            # Clean up the temporary directory if we created one
            if temp_dir:
                temp_dir.cleanup()

    def validate_yaml(self) -> List[str]:
        """
        Validate the playbook for YAML conversion.

        Returns:
            A list of validation errors, or an empty list if the playbook is valid for YAML conversion
        """
        errors = self.validate()

        # Additional validation for YAML conversion
        for play in self.plays:
            for task in play.tasks:
                task_errors = task.validate()
                if task_errors:
                    errors.append(f"Task '{task.name}' is invalid: {', '.join(task_errors)}")

            for handler in play.handlers:
                handler_errors = handler.validate()
                if handler_errors:
                    errors.append(f"Handler '{handler.name}' is invalid: {', '.join(handler_errors)}")

        for handler in self.handlers:
            handler_errors = handler.validate()
            if handler_errors:
                errors.append(f"Handler '{handler.name}' is invalid: {', '.join(handler_errors)}")

        return errors

    def is_valid_yaml(self) -> bool:
        """
        Check if the playbook is valid for YAML conversion.

        Returns:
            True if the playbook is valid for YAML conversion, False otherwise
        """
        return len(self.validate_yaml()) == 0


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


def to_yaml(obj: Any) -> str:
    """
    Convert an object to a YAML string.

    Args:
        obj: The object to convert

    Returns:
        A YAML string representation of the object

    Raises:
        AttributeError: If the object does not have a to_yaml method
        yaml.YAMLError: If the object cannot be converted to YAML
    """
    if hasattr(obj, "to_yaml"):
        return obj.to_yaml()
    elif isinstance(obj, dict):
        try:
            return yaml.dump(obj, default_flow_style=False)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Failed to convert dictionary to YAML: {e}")
    elif isinstance(obj, list):
        try:
            return yaml.dump(obj, default_flow_style=False)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Failed to convert list to YAML: {e}")
    else:
        raise AttributeError(f"Object of type {type(obj).__name__} does not have a to_yaml method")


def to_yaml_file(obj: Any, file_path: Union[str, Path], mode: str = "w") -> None:
    """
    Write an object to a YAML file.

    Args:
        obj: The object to write
        file_path: The path to the file to write to
        mode: The mode to open the file in (default: "w")

    Raises:
        AttributeError: If the object does not have a to_yaml method
        yaml.YAMLError: If the object cannot be converted to YAML
        IOError: If the file cannot be written to
    """
    yaml_str = to_yaml(obj)

    try:
        with open(file_path, mode) as f:
            f.write(yaml_str)
    except IOError as e:
        raise IOError(f"Failed to write YAML to file '{file_path}': {e}")


def run_playbook(
    playbook: Union[Playbook, Dict[str, Any], str, Path],
    inventory: Optional[Union[str, Dict[str, Any]]] = None,
    private_data_dir: Optional[str] = None,
    **kwargs: Any
) -> TaskResult:
    """
    Run an Ansible playbook using ansible_runner.

    Args:
        playbook: The playbook to run (Playbook object, dictionary, or path to playbook file)
        inventory: The inventory to use (path to inventory file or inventory dict)
        private_data_dir: The private data directory to use
        **kwargs: Additional arguments to pass to ansible_runner.run()

    Returns:
        The result of running the playbook

    Raises:
        ValueError: If the playbook is invalid
        TypeError: If the playbook is not a Playbook, dictionary, or string
    """
    # If playbook is a Playbook object, use its run_with_runner method
    if isinstance(playbook, Playbook):
        return playbook.run_with_runner(
            inventory=inventory,
            private_data_dir=private_data_dir,
            **kwargs
        )

    # Create a temporary directory for the playbook if no private_data_dir is provided
    temp_dir = None
    if not private_data_dir:
        temp_dir = tempfile.TemporaryDirectory()
        private_data_dir = temp_dir.name

    try:
        # Set up the playbook
        if isinstance(playbook, dict):
            # Use the provided playbook dictionary
            playbook_dict = playbook
        elif isinstance(playbook, (str, Path)):
            # Use the provided playbook file
            playbook_path = str(playbook)
        else:
            raise TypeError("Playbook must be a Playbook object, dictionary, or path to a playbook file")

        # Set up the inventory
        if inventory:
            if isinstance(inventory, dict):
                # Create inventory file in the private data dir
                os.makedirs(os.path.join(private_data_dir, "inventory"), exist_ok=True)
                with open(os.path.join(private_data_dir, "inventory", "hosts"), "w") as f:
                    yaml.dump(inventory, f)
            else:
                # Use the provided inventory file
                kwargs["inventory"] = inventory

        # Run the playbook
        if isinstance(playbook, dict):
            result = ansible_runner.run(
                private_data_dir=private_data_dir,
                playbook=playbook_dict,
                **kwargs
            )
        else:
            result = ansible_runner.run(
                private_data_dir=private_data_dir,
                playbook=playbook_path,
                **kwargs
            )

        # Convert the result to a TaskResult
        return TaskResult(
            success=(result.rc == 0),
            changed=any(event.get("event_data", {}).get("changed", False) 
                       for event in result.events if event.get("event") == "runner_on_ok"),
            error=result.stderr if result.rc != 0 else None,
            output={
                "rc": result.rc,
                "status": result.status,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "events": [event for event in result.events],
                "stats": result.stats
            }
        )
    finally:
        # Clean up the temporary directory if we created one
        if temp_dir:
            temp_dir.cleanup()


def run_playbook_with_runner(
    playbook_content: Union[str, Dict[str, Any]],
    inventory_content: Optional[Dict[str, Any]] = None,
    private_data_dir: Optional[str] = None,
    **kwargs: Any
) -> TaskResult:
    """
    Run an Ansible playbook using ansible_runner with provided content.

    Args:
        playbook_content: The content of the playbook (YAML string or dictionary)
        inventory_content: The content of the inventory (dictionary)
        private_data_dir: The private data directory to use
        **kwargs: Additional arguments to pass to ansible_runner.run()

    Returns:
        The result of running the playbook

    Raises:
        ValueError: If the playbook content is invalid
    """
    # Create a temporary directory for the playbook if no private_data_dir is provided
    temp_dir = None
    if not private_data_dir:
        temp_dir = tempfile.TemporaryDirectory()
        private_data_dir = temp_dir.name

    try:
        # Set up the playbook
        os.makedirs(os.path.join(private_data_dir, "project"), exist_ok=True)
        playbook_path = os.path.join(private_data_dir, "project", "playbook.yml")

        if isinstance(playbook_content, dict):
            # Convert dictionary to YAML
            with open(playbook_path, "w") as f:
                yaml.dump(playbook_content, f)
        elif isinstance(playbook_content, str):
            # Write YAML string to file
            with open(playbook_path, "w") as f:
                f.write(playbook_content)
        else:
            raise TypeError("Playbook content must be a dictionary or YAML string")

        # Set up the inventory
        if inventory_content:
            os.makedirs(os.path.join(private_data_dir, "inventory"), exist_ok=True)
            with open(os.path.join(private_data_dir, "inventory", "hosts"), "w") as f:
                yaml.dump(inventory_content, f)

        # Run the playbook
        result = ansible_runner.run(
            private_data_dir=private_data_dir,
            playbook="playbook.yml",
            **kwargs
        )

        # Convert the result to a TaskResult
        return TaskResult(
            success=(result.rc == 0),
            changed=any(event.get("event_data", {}).get("changed", False) 
                       for event in result.events if event.get("event") == "runner_on_ok"),
            error=result.stderr if result.rc != 0 else None,
            output={
                "rc": result.rc,
                "status": result.status,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "events": [event for event in result.events],
                "stats": result.stats
            }
        )
    finally:
        # Clean up the temporary directory if we created one
        if temp_dir:
            temp_dir.cleanup()
