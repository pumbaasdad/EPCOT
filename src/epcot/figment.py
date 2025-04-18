"""Figment module for EPCOT.

This module provides the Figment abstract base class that all figments must inherit
from.
"""

import os
from abc import ABC
from pathlib import Path
from typing import Dict, Any, List, Optional

from adk.task import Task
from epcot.config import get_figment_config
from epcot.utils import pascal_to_kebab


class Directory:
    """Directory configuration for a figment."""

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize a directory.

        Args:
            config: Configuration for the directory.
        """
        self.config = config


class Service:
    """Service configuration for a figment."""

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize a service.

        Args:
            config: Configuration for the service.
        """
        self.config = config


class PipModule:
    """Pip module configuration for a figment."""

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize a pip module.

        Args:
            config: Configuration for the pip module.
        """
        self.config = config


class Group:
    """Group configuration for a figment."""

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize a group.

        Args:
            config: Configuration for the group.
        """
        self.config = config


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

        # Load the figment.yaml file
        figment_name = pascal_to_kebab(self.__class__.__name__)
        figment_config_dir = Path(os.getcwd())
        try:
            self.figment_config = get_figment_config(figment_name, figment_config_dir)
        except FileNotFoundError:
            self.figment_config = {}

    def directories(self) -> List[Directory]:
        """Get the directories for this figment.

        Returns:
            A list of Directory objects.
        """
        directories = self.figment_config.get('directories', [])
        return [Directory(d) for d in directories]

    def files(self) -> List[Task]:
        """Get the files for this figment.

        Returns:
            A list of Task objects.
        """
        files = self.figment_config.get('files', [])
        return [Task(f) for f in files]

    def deb_repos(self) -> List[Task]:
        """Get the deb repos for this figment.

        Returns:
            A list of Task objects.
        """
        deb_repos = self.figment_config.get('deb_repos', [])
        return [Task(d) for d in deb_repos]

    def apt_keys(self) -> List[Task]:
        """Get the apt keys for this figment.

        Returns:
            A list of Task objects.
        """
        apt_keys = self.figment_config.get('apt_keys', [])
        return [Task(a) for a in apt_keys]

    def packages(self) -> List[str]:
        """Get the packages for this figment.

        Returns:
            A list of package names.
        """
        return self.figment_config.get('packages', [])

    def services(self) -> List[Service]:
        """Get the services for this figment.

        Returns:
            A list of Service objects.
        """
        services = []
        return self.figment_config.get('services', [])

    def pip_modules(self) -> List[PipModule]:
        """Get the pip modules for this figment.

        Returns:
            A list of PipModule objects.
        """
        pip_modules = self.figment_config.get('pip_modules', [])
        return [PipModule(p) for p in pip_modules]

    def users(self) -> List[str]:
        """Get the users for this figment.

        Returns:
            A list of user names.
        """
        return self.figment_config.get('users', [])

    def groups(self) -> List[Group]:
        """Get the groups for this figment.

        Returns:
            A list of Group objects.
        """
        groups = self.figment_config.get('groups', [])
        return [Group(g) for g in groups]

    def apt_ppas(self) -> List[Task]:
        """Get the apt PPAs for this figment.

        Returns:
            A list of Task objects.
        """
        apt_ppas = self.figment_config.get('apt_ppas', [])
        return [Task(a) for a in apt_ppas]
