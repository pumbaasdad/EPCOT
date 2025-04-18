"""Tests for the Figment module."""

import os
import unittest
from pathlib import Path

from epcot.figments.backup import Backup


class TestFigment(unittest.TestCase):
    """Tests for the Figment module."""

    def setUp(self) -> None:
        """Set up the test environment."""
        # Change to the project root directory
        os.chdir(Path(__file__).parent.parent)

    def test_backup_directories_is_list(self) -> None:
        """Test the Backup figment directories method returns a list."""
        backup = Backup()
        directories = backup.directories()
        self.assertIsInstance(directories, list)

    def test_backup_directories_config_is_dict(self) -> None:
        """Test the Backup figment directories config is a dict if directories exist."""
        backup = Backup()
        directories = backup.directories()
        if directories:
            self.assertIsInstance(directories[0].config, dict)

    def test_backup_directories_config_has_path(self) -> None:
        """Test the Backup figment directories config has path if directories exist."""
        backup = Backup()
        directories = backup.directories()
        if directories:
            self.assertIn("path", directories[0].config)

    def test_backup_files_is_list(self) -> None:
        """Test the Backup figment files method returns a list."""
        backup = Backup()
        files = backup.files()
        self.assertIsInstance(files, list)

    def test_backup_files_config_is_dict(self) -> None:
        """Test the Backup figment files config is a dict if files exist."""
        backup = Backup()
        files = backup.files()
        if files:
            self.assertIsInstance(files[0].config, dict)

    def test_backup_files_config_has_src(self) -> None:
        """Test the Backup figment files config has src if files exist."""
        backup = Backup()
        files = backup.files()
        if files:
            self.assertIn("src", files[0].config)

    def test_backup_files_config_has_dest(self) -> None:
        """Test the Backup figment files config has dest if files exist."""
        backup = Backup()
        files = backup.files()
        if files:
            self.assertIn("dest", files[0].config)

    def test_backup_services_is_list(self) -> None:
        """Test the Backup figment services method returns a list."""
        backup = Backup()
        services = backup.services()
        self.assertIsInstance(services, list)

    def test_backup_services_config_is_dict(self) -> None:
        """Test the Backup figment services config is a dict if services exist."""
        backup = Backup()
        services = backup.services()
        if services:
            self.assertIsInstance(services[0].config, dict)

    def test_backup_services_config_has_name(self) -> None:
        """Test the Backup figment services config has name if services exist."""
        backup = Backup()
        services = backup.services()
        if services:
            self.assertIn("name", services[0].config)

    def test_backup_packages_is_list(self) -> None:
        """Test the Backup figment packages method returns a list."""
        backup = Backup()
        self.assertIsInstance(backup.packages(), list)

    def test_backup_users_is_list(self) -> None:
        """Test the Backup figment users method returns a list."""
        backup = Backup()
        self.assertIsInstance(backup.users(), list)

    def test_backup_groups_is_list(self) -> None:
        """Test the Backup figment groups method returns a list."""
        backup = Backup()
        self.assertIsInstance(backup.groups(), list)

    def test_backup_pip_modules_is_list(self) -> None:
        """Test the Backup figment pip_modules method returns a list."""
        backup = Backup()
        self.assertIsInstance(backup.pip_modules(), list)

    def test_backup_deb_repos_is_list(self) -> None:
        """Test the Backup figment deb_repos method returns a list."""
        backup = Backup()
        self.assertIsInstance(backup.deb_repos(), list)

    def test_backup_apt_keys_is_list(self) -> None:
        """Test the Backup figment apt_keys method returns a list."""
        backup = Backup()
        self.assertIsInstance(backup.apt_keys(), list)

    def test_backup_apt_ppas_is_list(self) -> None:
        """Test the Backup figment apt_ppas method returns a list."""
        backup = Backup()
        self.assertIsInstance(backup.apt_ppas(), list)


if __name__ == "__main__":
    unittest.main()
