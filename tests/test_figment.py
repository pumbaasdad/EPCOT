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

    def test_backup_figment(self) -> None:
        """Test the Backup figment."""
        backup = Backup()

        # Test directories
        directories = backup.directories()
        self.assertIsInstance(directories, list)
        if directories:
            self.assertIsInstance(directories[0].config, dict)
            self.assertIn("path", directories[0].config)

        # Test files
        files = backup.files()
        self.assertIsInstance(files, list)
        if files:
            self.assertIsInstance(files[0].config, dict)
            self.assertIn("src", files[0].config)
            self.assertIn("dest", files[0].config)

        # Test services
        services = backup.services()
        self.assertIsInstance(services, list)
        if services:
            self.assertIsInstance(services[0].config, dict)
            self.assertIn("name", services[0].config)

        # Test other methods
        self.assertIsInstance(backup.packages(), list)
        self.assertIsInstance(backup.users(), list)
        self.assertIsInstance(backup.groups(), list)
        self.assertIsInstance(backup.pip_modules(), list)
        self.assertIsInstance(backup.deb_repos(), list)
        self.assertIsInstance(backup.apt_keys(), list)
        self.assertIsInstance(backup.apt_ppas(), list)


if __name__ == "__main__":
    unittest.main()
