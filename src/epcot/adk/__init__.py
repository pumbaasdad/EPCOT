"""
Ansible Development Kit (ADK) module.

This module provides a programmatic interface for creating and managing Ansible tasks and playbooks.
"""

from typing import Dict, List, Optional, Union, Any, Set
from collections import defaultdict

__all__ = ["Task", "Play", "Playbook", "TaskResult", "Handler"]


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
