"""
Client module for EPCOT.

This module provides interfaces for working with Figments - reusable components
that provide various system configurations.
"""

from typing import Dict, List, Optional, Any, Union

__all__ = ["Figment", "FigmentClient", "FigmentResult"]


class Figment:
    """
    Represents a Figment - a reusable component that provides a system configuration.
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        path: str,
    ) -> None:
        """
        Initialize a Figment.
        
        Args:
            name: The name of the figment
            description: A description of what the figment does
            path: Path to the figment's directory
        """
        self.name = name
        self.description = description
        self.path = path
    
    def apply(
        self,
        hosts: Union[str, List[str]],
        variables: Optional[Dict[str, Any]] = None,
    ) -> "FigmentResult":
        """
        Apply the figment to the specified hosts.
        
        Args:
            hosts: The hosts to apply the figment to
            variables: Variables to use when applying the figment
            
        Returns:
            The result of applying the figment
        """
        # This would be implemented to actually apply the figment
        return FigmentResult(success=True)


class FigmentClient:
    """
    Client for working with Figments.
    """
    
    def __init__(
        self,
        config: Optional[Any] = None,
    ) -> None:
        """
        Initialize a FigmentClient.
        
        Args:
            config: Configuration for the client
        """
        self.config = config
    
    def load_figment(self, name: str) -> Figment:
        """
        Load a figment by name.
        
        Args:
            name: The name of the figment to load
            
        Returns:
            The loaded figment
            
        Raises:
            ValueError: If the figment cannot be found
        """
        # This would be implemented to actually load the figment
        return Figment(
            name=name,
            description=f"Figment {name}",
            path=f"/path/to/figments/{name}",
        )
    
    def list_figments(self) -> List[str]:
        """
        List all available figments.
        
        Returns:
            A list of figment names
        """
        # This would be implemented to actually list the figments
        return ["nginx", "docker", "mysql"]


class FigmentResult:
    """
    Represents the result of applying a figment.
    """
    
    def __init__(
        self,
        success: bool,
        changed: bool = False,
        error: Optional[str] = None,
        output: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize a FigmentResult.
        
        Args:
            success: Whether the figment was applied successfully
            changed: Whether applying the figment changed the system
            error: Error message if applying the figment failed
            output: Output from applying the figment
        """
        self.success = success
        self.changed = changed
        self.error = error
        self.output = output or {}