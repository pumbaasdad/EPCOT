"""
Tests for the ADK module.
"""

import pytest
from epcot.adk import Task, Playbook, TaskResult


def test_task_creation():
    """Test that a Task can be created with the correct attributes."""
    task = Task(
        name="Install nginx",
        module="apt",
        args={"name": "nginx", "state": "present"},
        when="ansible_distribution == 'Ubuntu'",
        register="nginx_install",
        tags=["web", "nginx"],
    )
    
    assert task.name == "Install nginx"
    assert task.module == "apt"
    assert task.args == {"name": "nginx", "state": "present"}
    assert task.when == "ansible_distribution == 'Ubuntu'"
    assert task.register == "nginx_install"
    assert task.tags == ["web", "nginx"]


def test_playbook_creation():
    """Test that a Playbook can be created with the correct attributes."""
    playbook = Playbook(
        name="Setup Web Server",
        hosts="web_servers",
        become=True,
        vars={"nginx_version": "1.18.0"},
    )
    
    assert playbook.name == "Setup Web Server"
    assert playbook.hosts == "web_servers"
    assert playbook.become is True
    assert playbook.vars == {"nginx_version": "1.18.0"}
    assert playbook.tasks == []


def test_add_task_to_playbook():
    """Test that a Task can be added to a Playbook."""
    task = Task(
        name="Install nginx",
        module="apt",
        args={"name": "nginx", "state": "present"},
    )
    
    playbook = Playbook(
        name="Setup Web Server",
        hosts="web_servers",
    )
    
    playbook.add_task(task)
    
    assert len(playbook.tasks) == 1
    assert playbook.tasks[0] == task


def test_task_result_creation():
    """Test that a TaskResult can be created with the correct attributes."""
    result = TaskResult(
        success=True,
        changed=True,
        error=None,
        output={"status": "ok", "changed": True},
    )
    
    assert result.success is True
    assert result.changed is True
    assert result.error is None
    assert result.output == {"status": "ok", "changed": True}


def test_playbook_run():
    """Test that a Playbook can be run and returns a TaskResult."""
    playbook = Playbook(
        name="Setup Web Server",
        hosts="web_servers",
    )
    
    result = playbook.run()
    
    assert isinstance(result, TaskResult)
    assert result.success is True