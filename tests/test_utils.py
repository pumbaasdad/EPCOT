"""Tests for the utils module."""

import unittest

from epcot.utils import pascal_to_kebab


class TestUtils(unittest.TestCase):
    """Tests for the utils module."""

    def test_pascal_to_kebab(self) -> None:
        """Test the pascal_to_kebab function."""
        test_cases = [
            ("MediaServer", "media-server"),
            ("ReverseProxy", "reverse-proxy"),
            ("Backup", "backup"),
            ("HomeAutomation", "home-automation"),
            ("DNS", "dns"),
            ("DHCP", "dhcp"),
            ("IPTables", "ip-tables"),
            ("UniFi", "uni-fi"),
        ]

        for pascal_case, expected_kebab_case in test_cases:
            with self.subTest(pascal_case=pascal_case):
                self.assertEqual(pascal_to_kebab(pascal_case), expected_kebab_case)


if __name__ == "__main__":
    unittest.main()
