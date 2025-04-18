Usage
=====

Basic Usage
----------

EPCOT provides a programmatic interface for creating and managing Ansible tasks and playbooks.

Here's a simple example of how to use EPCOT:

.. code-block:: python

    from epcot.adk import Task, Playbook

    # Create a task
    task = Task(
        name="Install nginx",
        module="apt",
        args={"name": "nginx", "state": "present"},
    )

    # Create a playbook
    playbook = Playbook(
        name="Setup Web Server",
        hosts="web_servers",
    )

    # Add task to playbook
    playbook.add_task(task)

    # Run the playbook
    result = playbook.run()

    # Check the result
    if result.success:
        print("Nginx installed successfully!")
    else:
        print(f"Error: {result.error}")

Advanced Playbook Usage
---------------------

EPCOT provides advanced features for creating and managing Ansible playbooks:

.. code-block:: python

    from epcot.adk import Task, Handler, Play, Playbook

    # Create tasks
    install_task = Task(
        name="Install nginx",
        module="apt",
        args={"name": "nginx", "state": "present"},
    )

    config_task = Task(
        name="Configure nginx",
        module="template",
        args={"src": "nginx.conf.j2", "dest": "/etc/nginx/nginx.conf"},
    )

    start_task = Task(
        name="Start nginx",
        module="service",
        args={"name": "nginx", "state": "started"},
    )

    # Create a handler
    restart_handler = Handler(
        name="Restart nginx",
        module="service",
        args={"name": "nginx", "state": "restarted"},
    )

    # Create a playbook
    playbook = Playbook(
        name="Setup Web Server",
        hosts="web_servers",
        become=True,
        vars={"nginx_version": "1.18.0"},
    )

    # Create a play
    app_play = playbook.create_play(
        name="Configure App Servers",
        hosts="app_servers",
    )

    # Add tasks to the default play
    playbook.add_task(install_task)
    playbook.add_task(config_task)

    # Add tasks to a specific play
    playbook.add_task(start_task, app_play)

    # Add a handler
    playbook.add_handler(restart_handler)

    # Add dependencies between tasks
    playbook.add_dependency("Configure nginx", "Install nginx")
    playbook.add_dependency("Start nginx", "Configure nginx")

    # Set additional variables
    playbook.set_vars({"nginx_port": 80})

    # Validate the playbook
    if not playbook.is_valid():
        errors = playbook.validate()
        print(f"Playbook validation errors: {errors}")

    # Order tasks based on dependencies
    playbook.order_tasks()

    # Convert the playbook to a dictionary representation
    playbook_dict = playbook.to_dict()

    # Run the playbook
    result = playbook.run()

Working with Figments
--------------------

Figments are reusable components that provide various system configurations.

.. code-block:: python

    from epcot.client import Figment, FigmentClient

    # Initialize the client
    client = FigmentClient()

    # Load a figment
    nginx_figment = client.load_figment("nginx")

    # Apply the figment
    result = nginx_figment.apply(
        hosts=["web1.example.com", "web2.example.com"],
        variables={"nginx_version": "1.18.0"}
    )

    # Check the result
    if result.success:
        print("Nginx figment applied successfully!")
    else:
        print(f"Error: {result.error}")

Configuration
------------

EPCOT can be configured using a YAML file:

.. code-block:: yaml

    # epcot.yaml
    ansible:
      inventory: /path/to/inventory.yml
      private_key: /path/to/private_key

    figments:
      directory: /path/to/figments

    logging:
      level: INFO
      file: /path/to/epcot.log

Load the configuration in your code:

.. code-block:: python

    from epcot.config import Config

    # Load configuration
    config = Config.from_file("epcot.yaml")

    # Use the configuration
    client = FigmentClient(config=config)
