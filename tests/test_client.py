"""
Tests for the Client module.
"""

import pytest
from epcot.client import Figment, FigmentClient, FigmentResult


def test_figment_creation():
    """Test that a Figment can be created with the correct attributes."""
    figment = Figment(
        name="nginx",
        description="Installs and configures Nginx",
        path="/path/to/figments/nginx",
    )
    
    assert figment.name == "nginx"
    assert figment.description == "Installs and configures Nginx"
    assert figment.path == "/path/to/figments/nginx"


def test_figment_apply():
    """Test that a Figment can be applied and returns a FigmentResult."""
    figment = Figment(
        name="nginx",
        description="Installs and configures Nginx",
        path="/path/to/figments/nginx",
    )
    
    result = figment.apply(
        hosts=["web1.example.com", "web2.example.com"],
        variables={"nginx_version": "1.18.0"},
    )
    
    assert isinstance(result, FigmentResult)
    assert result.success is True


def test_figment_client_creation():
    """Test that a FigmentClient can be created."""
    client = FigmentClient()
    
    assert client.config is None
    
    # Test with config
    config = {"figments": {"directory": "/path/to/figments"}}
    client = FigmentClient(config=config)
    
    assert client.config == config


def test_figment_client_load_figment():
    """Test that a FigmentClient can load a Figment."""
    client = FigmentClient()
    
    figment = client.load_figment("nginx")
    
    assert isinstance(figment, Figment)
    assert figment.name == "nginx"


def test_figment_client_list_figments():
    """Test that a FigmentClient can list available Figments."""
    client = FigmentClient()
    
    figments = client.list_figments()
    
    assert isinstance(figments, list)
    assert "nginx" in figments
    assert "docker" in figments
    assert "mysql" in figments


def test_figment_result_creation():
    """Test that a FigmentResult can be created with the correct attributes."""
    result = FigmentResult(
        success=True,
        changed=True,
        error=None,
        output={"status": "ok", "changed": True},
    )
    
    assert result.success is True
    assert result.changed is True
    assert result.error is None
    assert result.output == {"status": "ok", "changed": True}