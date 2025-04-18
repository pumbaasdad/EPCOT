"""
Configuration module for EPCOT.

This module provides interfaces for loading and managing configuration.
"""

from typing import Dict, Any, Optional
import os
import yaml

__all__ = ["Config"]


class Config:
    """
    Configuration for EPCOT.
    """
    
    def __init__(
        self,
        ansible: Optional[Dict[str, Any]] = None,
        figments: Optional[Dict[str, Any]] = None,
        logging: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize a Config.
        
        Args:
            ansible: Ansible configuration
            figments: Figment configuration
            logging: Logging configuration
        """
        self.ansible = ansible or {}
        self.figments = figments or {}
        self.logging = logging or {}
    
    @classmethod
    def from_file(cls, path: str) -> "Config":
        """
        Load configuration from a file.
        
        Args:
            path: Path to the configuration file
            
        Returns:
            The loaded configuration
            
        Raises:
            FileNotFoundError: If the configuration file cannot be found
            yaml.YAMLError: If the configuration file is not valid YAML
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Configuration file not found: {path}")
        
        with open(path, "r") as f:
            config_data = yaml.safe_load(f)
        
        return cls(
            ansible=config_data.get("ansible"),
            figments=config_data.get("figments"),
            logging=config_data.get("logging"),
        )
    
    def get_ansible_config(self) -> Dict[str, Any]:
        """
        Get the Ansible configuration.
        
        Returns:
            The Ansible configuration
        """
        return self.ansible
    
    def get_figments_config(self) -> Dict[str, Any]:
        """
        Get the Figment configuration.
        
        Returns:
            The Figment configuration
        """
        return self.figments
    
    def get_logging_config(self) -> Dict[str, Any]:
        """
        Get the logging configuration.
        
        Returns:
            The logging configuration
        """
        return self.logging