"""
Tests for the ADK module.
"""

import pytest
from unittest.mock import patch, MagicMock
from epcot.adk import (
    Task, Play, Playbook, TaskResult, Handler, 
    to_yaml, to_yaml_file, run_playbook, run_playbook_with_runner
)


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


def test_handler_creation():
    """Test that a Handler can be created with the correct attributes."""
    handler = Handler(
        name="Restart nginx",
        module="service",
        args={"name": "nginx", "state": "restarted"},
        when="nginx_config_changed",
        tags=["web", "nginx"],
    )

    assert handler.name == "Restart nginx"
    assert handler.module == "service"
    assert handler.args == {"name": "nginx", "state": "restarted"}
    assert handler.when == "nginx_config_changed"
    assert handler.tags == ["web", "nginx"]


def test_play_creation():
    """Test that a Play can be created with the correct attributes."""
    play = Play(
        name="Setup Web Server",
        hosts="web_servers",
        become=True,
        vars={"nginx_version": "1.18.0"},
    )

    assert play.name == "Setup Web Server"
    assert play.hosts == "web_servers"
    assert play.become is True
    assert play.vars == {"nginx_version": "1.18.0"}
    assert play.tasks == []
    assert play.handlers == []
    assert play.dependencies == {}


def test_add_task_to_play():
    """Test that a Task can be added to a Play."""
    task = Task(
        name="Install nginx",
        module="apt",
        args={"name": "nginx", "state": "present"},
    )

    play = Play(
        name="Setup Web Server",
        hosts="web_servers",
    )

    play.add_task(task)

    assert len(play.tasks) == 1
    assert play.tasks[0] == task


def test_add_handler_to_play():
    """Test that a Handler can be added to a Play."""
    handler = Handler(
        name="Restart nginx",
        module="service",
        args={"name": "nginx", "state": "restarted"},
    )

    play = Play(
        name="Setup Web Server",
        hosts="web_servers",
    )

    play.add_handler(handler)

    assert len(play.handlers) == 1
    assert play.handlers[0] == handler


def test_add_dependency_to_play():
    """Test that a dependency can be added to a Play."""
    play = Play(
        name="Setup Web Server",
        hosts="web_servers",
    )

    play.add_dependency("Configure nginx", "Install nginx")

    assert play.dependencies == {"Configure nginx": ["Install nginx"]}


def test_play_to_dict():
    """Test that a Play can be converted to a dictionary representation."""
    task = Task(
        name="Install nginx",
        module="apt",
        args={"name": "nginx", "state": "present"},
        when="ansible_distribution == 'Ubuntu'",
        register="nginx_install",
        tags=["web", "nginx"],
    )

    handler = Handler(
        name="Restart nginx",
        module="service",
        args={"name": "nginx", "state": "restarted"},
    )

    play = Play(
        name="Setup Web Server",
        hosts="web_servers",
        become=True,
        vars={"nginx_version": "1.18.0"},
    )

    play.add_task(task)
    play.add_handler(handler)

    play_dict = play.to_dict()

    assert play_dict["name"] == "Setup Web Server"
    assert play_dict["hosts"] == "web_servers"
    assert play_dict["become"] is True
    assert play_dict["vars"] == {"nginx_version": "1.18.0"}
    assert len(play_dict["tasks"]) == 1
    assert play_dict["tasks"][0]["name"] == "Install nginx"
    assert play_dict["tasks"][0]["apt"] == {"name": "nginx", "state": "present"}
    assert play_dict["tasks"][0]["when"] == "ansible_distribution == 'Ubuntu'"
    assert play_dict["tasks"][0]["register"] == "nginx_install"
    assert play_dict["tasks"][0]["tags"] == ["web", "nginx"]
    assert len(play_dict["handlers"]) == 1
    assert play_dict["handlers"][0]["name"] == "Restart nginx"
    assert play_dict["handlers"][0]["service"] == {"name": "nginx", "state": "restarted"}


def test_playbook_default_play():
    """Test that a Playbook creates a default play when needed."""
    playbook = Playbook(
        name="Setup Web Server",
        hosts="web_servers",
        become=True,
        vars={"nginx_version": "1.18.0"},
    )

    # Access the default play
    default_play = playbook.default_play

    assert default_play.name == "Setup Web Server"
    assert default_play.hosts == "web_servers"
    assert default_play.become is True
    assert default_play.vars == {"nginx_version": "1.18.0"}
    assert len(playbook.plays) == 1
    assert playbook.plays[0] == default_play


def test_playbook_create_play():
    """Test that a Playbook can create a new play."""
    playbook = Playbook(
        name="Setup Web Server",
        hosts="web_servers",
        become=True,
        vars={"nginx_version": "1.18.0"},
    )

    play = playbook.create_play(
        name="Configure Web Server",
        hosts="app_servers",
        become=False,
        vars={"nginx_version": "1.20.0"},
    )

    assert play.name == "Configure Web Server"
    assert play.hosts == "app_servers"
    assert play.become is False
    assert play.vars == {"nginx_version": "1.20.0"}
    assert len(playbook.plays) == 1
    assert playbook.plays[0] == play


def test_playbook_add_play():
    """Test that a Playbook can add an existing play."""
    playbook = Playbook(
        name="Setup Web Server",
        hosts="web_servers",
    )

    play = Play(
        name="Configure Web Server",
        hosts="app_servers",
    )

    playbook.add_play(play)

    assert len(playbook.plays) == 1
    assert playbook.plays[0] == play


def test_playbook_add_task_to_play():
    """Test that a Playbook can add a task to a specific play."""
    playbook = Playbook(
        name="Setup Web Server",
        hosts="web_servers",
    )

    play = playbook.create_play(
        name="Configure Web Server",
        hosts="app_servers",
    )

    task = Task(
        name="Install nginx",
        module="apt",
        args={"name": "nginx", "state": "present"},
    )

    playbook.add_task(task, play)

    assert len(play.tasks) == 1
    assert play.tasks[0] == task


def test_playbook_add_task_to_default_play():
    """Test that a Playbook can add a task to the default play."""
    playbook = Playbook(
        name="Setup Web Server",
        hosts="web_servers",
    )

    task = Task(
        name="Install nginx",
        module="apt",
        args={"name": "nginx", "state": "present"},
    )

    playbook.add_task(task)

    assert len(playbook.default_play.tasks) == 1
    assert playbook.default_play.tasks[0] == task


def test_playbook_add_handler():
    """Test that a Playbook can add a handler."""
    playbook = Playbook(
        name="Setup Web Server",
        hosts="web_servers",
    )

    handler = Handler(
        name="Restart nginx",
        module="service",
        args={"name": "nginx", "state": "restarted"},
    )

    playbook.add_handler(handler)

    assert len(playbook.handlers) == 1
    assert playbook.handlers[0] == handler


def test_playbook_add_handler_to_play():
    """Test that a Playbook can add a handler to a specific play."""
    playbook = Playbook(
        name="Setup Web Server",
        hosts="web_servers",
    )

    play = playbook.create_play(
        name="Configure Web Server",
        hosts="app_servers",
    )

    handler = Handler(
        name="Restart nginx",
        module="service",
        args={"name": "nginx", "state": "restarted"},
    )

    playbook.add_handler(handler, play)

    assert len(play.handlers) == 1
    assert play.handlers[0] == handler


def test_playbook_add_dependency():
    """Test that a Playbook can add a dependency between tasks."""
    playbook = Playbook(
        name="Setup Web Server",
        hosts="web_servers",
    )

    playbook.add_dependency("Configure nginx", "Install nginx")

    assert playbook._task_dependencies == {"Configure nginx": ["Install nginx"]}


def test_playbook_add_dependency_to_play():
    """Test that a Playbook can add a dependency to a specific play."""
    playbook = Playbook(
        name="Setup Web Server",
        hosts="web_servers",
    )

    play = playbook.create_play(
        name="Configure Web Server",
        hosts="app_servers",
    )

    playbook.add_dependency("Configure nginx", "Install nginx", play)

    assert play.dependencies == {"Configure nginx": ["Install nginx"]}


def test_playbook_set_vars():
    """Test that a Playbook can set variables."""
    playbook = Playbook(
        name="Setup Web Server",
        hosts="web_servers",
        vars={"nginx_version": "1.18.0"},
    )

    playbook.set_vars({"nginx_port": 80, "nginx_version": "1.20.0"})

    assert playbook.vars == {"nginx_version": "1.20.0", "nginx_port": 80}


def test_playbook_validate():
    """Test that a Playbook can be validated."""
    playbook = Playbook(
        name="Setup Web Server",
        hosts="web_servers",
    )

    task1 = Task(
        name="Install nginx",
        module="apt",
        args={"name": "nginx", "state": "present"},
    )

    task2 = Task(
        name="Configure nginx",
        module="template",
        args={"src": "nginx.conf.j2", "dest": "/etc/nginx/nginx.conf"},
    )

    playbook.add_task(task1)
    playbook.add_task(task2)
    playbook.add_dependency("Configure nginx", "Install nginx")

    assert playbook.is_valid()
    assert playbook.validate() == []


def test_playbook_validate_errors():
    """Test that a Playbook validation can detect errors."""
    playbook = Playbook(
        name="Setup Web Server",
        hosts="web_servers",
    )

    task = Task(
        name="Install nginx",
        module="apt",
        args={"name": "nginx", "state": "present"},
    )

    playbook.add_task(task)
    playbook.add_dependency("Configure nginx", "Install nginx")

    assert not playbook.is_valid()
    errors = playbook.validate()
    assert len(errors) == 1
    assert "Dependency refers to non-existent task: Configure nginx" in errors[0]


def test_playbook_order_tasks():
    """Test that a Playbook can order tasks based on dependencies."""
    playbook = Playbook(
        name="Setup Web Server",
        hosts="web_servers",
    )

    task1 = Task(
        name="Install nginx",
        module="apt",
        args={"name": "nginx", "state": "present"},
    )

    task2 = Task(
        name="Configure nginx",
        module="template",
        args={"src": "nginx.conf.j2", "dest": "/etc/nginx/nginx.conf"},
    )

    task3 = Task(
        name="Start nginx",
        module="service",
        args={"name": "nginx", "state": "started"},
    )

    # Add tasks in reverse order
    playbook.add_task(task3)
    playbook.add_task(task2)
    playbook.add_task(task1)

    # Add dependencies
    playbook.add_dependency("Configure nginx", "Install nginx")
    playbook.add_dependency("Start nginx", "Configure nginx")

    # Order tasks
    playbook.order_tasks()

    # Check that tasks are in the correct order
    tasks = playbook.default_play.tasks
    assert len(tasks) == 3
    assert tasks[0].name == "Install nginx"
    assert tasks[1].name == "Configure nginx"
    assert tasks[2].name == "Start nginx"


def test_playbook_to_dict():
    """Test that a Playbook can be converted to a dictionary representation."""
    playbook = Playbook(
        name="Setup Web Server",
        hosts="web_servers",
        become=True,
        vars={"nginx_version": "1.18.0"},
    )

    task1 = Task(
        name="Install nginx",
        module="apt",
        args={"name": "nginx", "state": "present"},
    )

    task2 = Task(
        name="Configure nginx",
        module="template",
        args={"src": "nginx.conf.j2", "dest": "/etc/nginx/nginx.conf"},
    )

    handler = Handler(
        name="Restart nginx",
        module="service",
        args={"name": "nginx", "state": "restarted"},
    )

    playbook.add_task(task1)
    playbook.add_task(task2)
    playbook.add_handler(handler)
    playbook.add_dependency("Configure nginx", "Install nginx")

    playbook_dict = playbook.to_dict()

    assert len(playbook_dict) == 1  # One play
    play_dict = playbook_dict[0]
    assert play_dict["name"] == "Setup Web Server"
    assert play_dict["hosts"] == "web_servers"
    assert play_dict["become"] is True
    assert play_dict["vars"] == {"nginx_version": "1.18.0"}
    assert len(play_dict["tasks"]) == 2
    assert play_dict["tasks"][0]["name"] == "Install nginx"
    assert play_dict["tasks"][1]["name"] == "Configure nginx"
    assert len(play_dict["handlers"]) == 1
    assert play_dict["handlers"][0]["name"] == "Restart nginx"


def test_playbook_run():
    """Test that a Playbook can be run and returns a TaskResult."""
    playbook = Playbook(
        name="Setup Web Server",
        hosts="web_servers",
    )

    result = playbook.run()

    assert isinstance(result, TaskResult)
    assert result.success is True


def test_task_to_yaml():
    """Test that a Task can be converted to YAML."""
    task = Task(
        name="Install nginx",
        module="apt",
        args={"name": "nginx", "state": "present"},
        when="ansible_distribution == 'Ubuntu'",
        register="nginx_install",
        tags=["web", "nginx"],
    )

    yaml_str = task.to_yaml()

    assert isinstance(yaml_str, str)
    assert "name: Install nginx" in yaml_str
    assert "apt:" in yaml_str
    assert "name: nginx" in yaml_str
    assert "state: present" in yaml_str
    assert "when: ansible_distribution == 'Ubuntu'" in yaml_str
    assert "register: nginx_install" in yaml_str
    assert "tags:" in yaml_str
    assert "- web" in yaml_str
    assert "- nginx" in yaml_str


def test_playbook_to_yaml():
    """Test that a Playbook can be converted to YAML."""
    playbook = Playbook(
        name="Setup Web Server",
        hosts="web_servers",
        become=True,
        vars={"nginx_version": "1.18.0"},
    )

    task1 = Task(
        name="Install nginx",
        module="apt",
        args={"name": "nginx", "state": "present"},
    )

    task2 = Task(
        name="Configure nginx",
        module="template",
        args={"src": "nginx.conf.j2", "dest": "/etc/nginx/nginx.conf"},
    )

    handler = Handler(
        name="Restart nginx",
        module="service",
        args={"name": "nginx", "state": "restarted"},
    )

    playbook.add_task(task1)
    playbook.add_task(task2)
    playbook.add_handler(handler)
    playbook.add_dependency("Configure nginx", "Install nginx")

    yaml_str = playbook.to_yaml()

    assert isinstance(yaml_str, str)
    assert "name: Setup Web Server" in yaml_str
    assert "hosts: web_servers" in yaml_str
    assert "become: true" in yaml_str
    assert "vars:" in yaml_str
    assert "nginx_version: 1.18.0" in yaml_str
    assert "tasks:" in yaml_str
    assert "name: Install nginx" in yaml_str
    assert "apt:" in yaml_str
    assert "name: nginx" in yaml_str
    assert "state: present" in yaml_str
    assert "name: Configure nginx" in yaml_str
    assert "template:" in yaml_str
    assert "src: nginx.conf.j2" in yaml_str
    assert "dest: /etc/nginx/nginx.conf" in yaml_str
    assert "handlers:" in yaml_str
    assert "name: Restart nginx" in yaml_str
    assert "service:" in yaml_str
    assert "name: nginx" in yaml_str
    assert "state: restarted" in yaml_str


def test_to_yaml_function():
    """Test that the to_yaml function works correctly."""
    task = Task(
        name="Install nginx",
        module="apt",
        args={"name": "nginx", "state": "present"},
    )

    yaml_str = to_yaml(task)

    assert isinstance(yaml_str, str)
    assert "name: Install nginx" in yaml_str
    assert "apt:" in yaml_str
    assert "name: nginx" in yaml_str
    assert "state: present" in yaml_str

    # Test with a dictionary
    dict_obj = {"name": "Test", "value": 123}
    yaml_str = to_yaml(dict_obj)

    assert isinstance(yaml_str, str)
    assert "name: Test" in yaml_str
    assert "value: 123" in yaml_str

    # Test with a list
    list_obj = [{"name": "Item 1"}, {"name": "Item 2"}]
    yaml_str = to_yaml(list_obj)

    assert isinstance(yaml_str, str)
    assert "- name: Item 1" in yaml_str
    assert "- name: Item 2" in yaml_str

    # Test with an object that doesn't have a to_yaml method
    with pytest.raises(AttributeError):
        to_yaml(123)


def test_to_yaml_file(tmp_path):
    """Test that the to_yaml_file function works correctly."""
    task = Task(
        name="Install nginx",
        module="apt",
        args={"name": "nginx", "state": "present"},
    )

    file_path = tmp_path / "task.yaml"
    to_yaml_file(task, file_path)

    assert file_path.exists()
    with open(file_path, "r") as f:
        content = f.read()

    assert "name: Install nginx" in content
    assert "apt:" in content
    assert "name: nginx" in content
    assert "state: present" in content

    # Test with a dictionary
    dict_obj = {"name": "Test", "value": 123}
    file_path = tmp_path / "dict.yaml"
    to_yaml_file(dict_obj, file_path)

    assert file_path.exists()
    with open(file_path, "r") as f:
        content = f.read()

    assert "name: Test" in content
    assert "value: 123" in content

    # Test with a list
    list_obj = [{"name": "Item 1"}, {"name": "Item 2"}]
    file_path = tmp_path / "list.yaml"
    to_yaml_file(list_obj, file_path)

    assert file_path.exists()
    with open(file_path, "r") as f:
        content = f.read()

    assert "- name: Item 1" in content
    assert "- name: Item 2" in content

    # Test with an object that doesn't have a to_yaml method
    with pytest.raises(AttributeError):
        to_yaml_file(123, tmp_path / "invalid.yaml")

    # Test with an invalid file path
    with pytest.raises(IOError):
        to_yaml_file(task, "/invalid/path/task.yaml")


def test_task_to_runner_dict():
    """Test that a Task can be converted to an ansible_runner dictionary."""
    task = Task(
        name="Install nginx",
        module="apt",
        args={"name": "nginx", "state": "present"},
        when="ansible_distribution == 'Ubuntu'",
        register="nginx_install",
        tags=["web", "nginx"],
    )

    runner_dict = task.to_runner_dict()

    assert runner_dict["name"] == "Install nginx"
    assert runner_dict["apt"] == {"name": "nginx", "state": "present"}
    assert runner_dict["when"] == "ansible_distribution == 'Ubuntu'"
    assert runner_dict["register"] == "nginx_install"
    assert runner_dict["tags"] == ["web", "nginx"]


def test_playbook_to_runner_dict():
    """Test that a Playbook can be converted to an ansible_runner dictionary."""
    playbook = Playbook(
        name="Setup Web Server",
        hosts="web_servers",
        become=True,
        vars={"nginx_version": "1.18.0"},
    )

    task1 = Task(
        name="Install nginx",
        module="apt",
        args={"name": "nginx", "state": "present"},
    )

    task2 = Task(
        name="Configure nginx",
        module="template",
        args={"src": "nginx.conf.j2", "dest": "/etc/nginx/nginx.conf"},
    )

    handler = Handler(
        name="Restart nginx",
        module="service",
        args={"name": "nginx", "state": "restarted"},
    )

    playbook.add_task(task1)
    playbook.add_task(task2)
    playbook.add_handler(handler)
    playbook.add_dependency("Configure nginx", "Install nginx")

    runner_dict = playbook.to_runner_dict()

    assert "playbook" in runner_dict
    assert isinstance(runner_dict["playbook"], list)
    assert len(runner_dict["playbook"]) == 1  # One play

    play_dict = runner_dict["playbook"][0]
    assert play_dict["name"] == "Setup Web Server"
    assert play_dict["hosts"] == "web_servers"
    assert play_dict["become"] is True
    assert play_dict["vars"] == {"nginx_version": "1.18.0"}
    assert len(play_dict["tasks"]) == 2
    assert play_dict["tasks"][0]["name"] == "Install nginx"
    assert play_dict["tasks"][1]["name"] == "Configure nginx"
    assert len(play_dict["handlers"]) == 1
    assert play_dict["handlers"][0]["name"] == "Restart nginx"


def test_task_validate_runner():
    """Test that a Task can be validated for ansible_runner."""
    task = Task(
        name="Install nginx",
        module="apt",
        args={"name": "nginx", "state": "present"},
    )

    assert task.is_valid_runner()
    assert task.validate_runner() == []

    # Test with invalid task
    invalid_task = Task(
        name="",  # Empty name is invalid
        module="apt",
        args={"name": "nginx", "state": "present"},
    )

    assert not invalid_task.is_valid_runner()
    errors = invalid_task.validate_runner()
    assert len(errors) == 1
    assert "Task must have a name" in errors[0]


def test_playbook_validate_runner():
    """Test that a Playbook can be validated for ansible_runner."""
    playbook = Playbook(
        name="Setup Web Server",
        hosts="web_servers",
    )

    task = Task(
        name="Install nginx",
        module="apt",
        args={"name": "nginx", "state": "present"},
    )

    playbook.add_task(task)

    assert playbook.is_valid_runner()
    assert playbook.validate_runner() == []

    # Test with invalid task
    invalid_playbook = Playbook(
        name="Setup Web Server",
        hosts="web_servers",
    )

    invalid_task = Task(
        name="",  # Empty name is invalid
        module="apt",
        args={"name": "nginx", "state": "present"},
    )

    invalid_playbook.add_task(invalid_task)

    assert not invalid_playbook.is_valid_runner()
    errors = invalid_playbook.validate_runner()
    assert len(errors) == 1
    assert "Task '' is invalid for ansible_runner" in errors[0]


@patch("ansible_runner.run")
def test_playbook_run_with_runner(mock_run):
    """Test that a Playbook can be run with ansible_runner."""
    # Set up the mock
    mock_result = MagicMock()
    mock_result.rc = 0
    mock_result.status = "successful"
    mock_result.stdout = "Playbook ran successfully"
    mock_result.stderr = ""
    mock_result.events = [
        {"event": "runner_on_ok", "event_data": {"changed": True}},
        {"event": "runner_on_ok", "event_data": {"changed": False}},
    ]
    mock_result.stats = {"ok": 2, "changed": 1, "failures": 0}
    mock_run.return_value = mock_result

    # Create a playbook
    playbook = Playbook(
        name="Setup Web Server",
        hosts="web_servers",
    )

    task = Task(
        name="Install nginx",
        module="apt",
        args={"name": "nginx", "state": "present"},
    )

    playbook.add_task(task)

    # Run the playbook
    result = playbook.run_with_runner()

    # Check that ansible_runner.run was called
    mock_run.assert_called_once()

    # Check the result
    assert result.success is True
    assert result.changed is True
    assert result.error is None
    assert result.output["rc"] == 0
    assert result.output["status"] == "successful"
    assert result.output["stdout"] == "Playbook ran successfully"
    assert result.output["stderr"] == ""
    assert len(result.output["events"]) == 2
    assert result.output["stats"] == {"ok": 2, "changed": 1, "failures": 0}

    # Test with invalid playbook
    invalid_playbook = Playbook(
        name="Setup Web Server",
        hosts="web_servers",
    )

    invalid_task = Task(
        name="",  # Empty name is invalid
        module="apt",
        args={"name": "nginx", "state": "present"},
    )

    invalid_playbook.add_task(invalid_task)

    # Run the invalid playbook
    with pytest.raises(ValueError):
        invalid_playbook.run_with_runner()


@patch("ansible_runner.run")
def test_run_playbook(mock_run):
    """Test that a playbook can be run with the run_playbook function."""
    # Set up the mock
    mock_result = MagicMock()
    mock_result.rc = 0
    mock_result.status = "successful"
    mock_result.stdout = "Playbook ran successfully"
    mock_result.stderr = ""
    mock_result.events = [
        {"event": "runner_on_ok", "event_data": {"changed": True}},
        {"event": "runner_on_ok", "event_data": {"changed": False}},
    ]
    mock_result.stats = {"ok": 2, "changed": 1, "failures": 0}
    mock_run.return_value = mock_result

    # Create a playbook
    playbook = Playbook(
        name="Setup Web Server",
        hosts="web_servers",
    )

    task = Task(
        name="Install nginx",
        module="apt",
        args={"name": "nginx", "state": "present"},
    )

    playbook.add_task(task)

    # Run the playbook
    result = run_playbook(playbook)

    # Check that ansible_runner.run was called
    mock_run.assert_called_once()

    # Check the result
    assert result.success is True
    assert result.changed is True
    assert result.error is None
    assert result.output["rc"] == 0
    assert result.output["status"] == "successful"
    assert result.output["stdout"] == "Playbook ran successfully"
    assert result.output["stderr"] == ""
    assert len(result.output["events"]) == 2
    assert result.output["stats"] == {"ok": 2, "changed": 1, "failures": 0}

    # Reset the mock
    mock_run.reset_mock()

    # Test with a dictionary
    playbook_dict = {
        "name": "Setup Web Server",
        "hosts": "web_servers",
        "tasks": [
            {
                "name": "Install nginx",
                "apt": {"name": "nginx", "state": "present"},
            }
        ]
    }

    # Run the playbook
    result = run_playbook(playbook_dict)

    # Check that ansible_runner.run was called
    mock_run.assert_called_once()

    # Check the result
    assert result.success is True
    assert result.changed is True
    assert result.error is None

    # Reset the mock
    mock_run.reset_mock()

    # Test with a file path
    result = run_playbook("path/to/playbook.yml")

    # Check that ansible_runner.run was called
    mock_run.assert_called_once()

    # Check the result
    assert result.success is True
    assert result.changed is True
    assert result.error is None

    # Test with an invalid type
    with pytest.raises(TypeError):
        run_playbook(123)


@patch("ansible_runner.run")
def test_run_playbook_with_runner(mock_run):
    """Test that a playbook can be run with the run_playbook_with_runner function."""
    # Set up the mock
    mock_result = MagicMock()
    mock_result.rc = 0
    mock_result.status = "successful"
    mock_result.stdout = "Playbook ran successfully"
    mock_result.stderr = ""
    mock_result.events = [
        {"event": "runner_on_ok", "event_data": {"changed": True}},
        {"event": "runner_on_ok", "event_data": {"changed": False}},
    ]
    mock_result.stats = {"ok": 2, "changed": 1, "failures": 0}
    mock_run.return_value = mock_result

    # Create a playbook dictionary
    playbook_dict = {
        "name": "Setup Web Server",
        "hosts": "web_servers",
        "tasks": [
            {
                "name": "Install nginx",
                "apt": {"name": "nginx", "state": "present"},
            }
        ]
    }

    # Run the playbook
    result = run_playbook_with_runner(playbook_dict)

    # Check that ansible_runner.run was called
    mock_run.assert_called_once()

    # Check the result
    assert result.success is True
    assert result.changed is True
    assert result.error is None
    assert result.output["rc"] == 0
    assert result.output["status"] == "successful"
    assert result.output["stdout"] == "Playbook ran successfully"
    assert result.output["stderr"] == ""
    assert len(result.output["events"]) == 2
    assert result.output["stats"] == {"ok": 2, "changed": 1, "failures": 0}

    # Reset the mock
    mock_run.reset_mock()

    # Test with a YAML string
    playbook_yaml = """
    - name: Setup Web Server
      hosts: web_servers
      tasks:
        - name: Install nginx
          apt:
            name: nginx
            state: present
    """

    # Run the playbook
    result = run_playbook_with_runner(playbook_yaml)

    # Check that ansible_runner.run was called
    mock_run.assert_called_once()

    # Check the result
    assert result.success is True
    assert result.changed is True
    assert result.error is None

    # Test with an invalid type
    with pytest.raises(TypeError):
        run_playbook_with_runner(123)
