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