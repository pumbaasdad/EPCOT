"""
EPCOT - Experimental Prototype Configuration of Tomorrow.

A system for managing infrastructure using Ansible.
"""

__version__ = "0.1.0"

from . import adk
from . import client
from . import config

__all__ = ["adk", "client", "config"]
