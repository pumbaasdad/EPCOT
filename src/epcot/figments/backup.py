"""Backup figment for EPCOT.

This figment provides backup functionality for EPCOT.
"""

from epcot import Figment


class Backup(Figment):
    """Backup figment for EPCOT.

    This figment provides backup functionality for EPCOT.
    """

    def run(self) -> None:
        """Run the backup figment.

        This method is called by the EPCOT CLI to execute the backup functionality.
        """
        print("Running backup figment")
        print(f"Configuration: {self.config}")
