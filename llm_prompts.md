# EPCOT Implementation Prompts for Code-Generation LLM

This document provides a series of prompts for a code-generation LLM to implement the EPCOT project in a test-driven manner. Each prompt builds on the previous ones and focuses on implementing a specific step in the implementation plan.

## Phase 1: Project Setup and Core Infrastructure

### Prompt 1.1: Initial Project Setup

```
I'm building a Python project called EPCOT that will be a system for managing infrastructure using Ansible. I need to set up the initial project structure using Poetry.

Requirements:
- Python 3.12.3
- Poetry for dependency management
- Black for code formatting
- Flake8 for linting
- Pytest for testing
- Sphinx for documentation
- Type hints throughout the codebase

Please create:
1. A pyproject.toml file with the necessary dependencies and configuration
2. A basic project structure with src/epcot directory and tests directory
3. Configuration files for Black, Flake8, and Pytest
4. A basic README.md with project overview
5. A basic Sphinx documentation setup

The project should follow best practices for Python package development and be set up for test-driven development.
```

### Prompt 1.2: Core Type Definitions

```
Now I need to define the core types and interfaces for the EPCOT project. This project has two main components:

1. An Ansible Development Kit (ADK) - A programmatic interface for creating Ansible tasks and playbooks
2. A client that uses the ADK to manage "Figments" (modular components that provide various system configurations)

Please create:
1. Base types and interfaces for the ADK component
   - Task interface
   - Playbook interface
   - TaskResult interface
2. Base types and interfaces for the client component
   - Figment interface
   - FigmentResult interface
   - Configuration interfaces

All types should be properly annotated with type hints and documented with docstrings. Include abstract base classes where appropriate.

Also, set up mypy configuration for type checking and add type checking to the CI pipeline.
```

### Prompt 1.3: Basic Testing Infrastructure

```
Now I need to set up the basic testing infrastructure for the EPCOT project. This should include test fixtures, helpers, and basic test cases for the core functionality.

Please create:
1. Test fixtures for:
   - Creating temporary directories for test files
   - Creating sample YAML configurations
   - Mocking Ansible runner
2. Test helpers for:
   - Validating task outputs
   - Comparing YAML files
   - Checking type correctness
3. Basic test cases for:
   - Task interface
   - Playbook interface
   - Figment interface

The tests should follow best practices for pytest and be designed to support test-driven development of the rest of the project.
```

## Phase 2: Ansible Development Kit (ADK)

### Prompt 2.1: Base Task Class

```
Now I need to implement the base Task class for the Ansible Development Kit (ADK) component of the EPCOT project. This class will be the foundation for all Ansible tasks in the system.

Based on the previously defined interfaces, please implement:
1. An abstract BaseTask class that implements the Task interface
2. Common task properties and methods:
   - name
   - module
   - arguments
   - when condition
   - tags
   - register variable
   - ignore_errors flag
   - become flag
3. Basic task validation methods
4. Methods for converting the task to a dictionary representation

Include comprehensive unit tests for all functionality, following the test-driven development approach. The implementation should be properly typed and documented with docstrings.
```

### Prompt 2.2: Playbook Class

```
Now I need to implement the Playbook class for the Ansible Development Kit (ADK) component of the EPCOT project. This class will be responsible for managing collections of tasks and generating Ansible playbooks.

Based on the previously defined interfaces and the BaseTask class, please implement:
1. A Playbook class that implements the Playbook interface
2. Methods for:
   - Adding tasks to the playbook
   - Organizing tasks into plays
   - Setting playbook-level variables
   - Setting playbook-level handlers
   - Ordering tasks based on dependencies
3. Validation methods for ensuring the playbook is valid
4. Methods for converting the playbook to a dictionary representation

Include comprehensive unit tests for all functionality, following the test-driven development approach. The implementation should be properly typed and documented with docstrings.
```

### Prompt 2.3: Task to YAML Conversion

```
Now I need to implement the functionality to convert Task and Playbook objects to YAML for the Ansible Development Kit (ADK) component of the EPCOT project.

Based on the previously implemented BaseTask and Playbook classes, please implement:
1. Methods for converting Task objects to YAML
2. Methods for converting Playbook objects to YAML
3. Validation during the conversion process to ensure the generated YAML is valid
4. Utility functions for writing the YAML to files

Include comprehensive unit tests for all functionality, following the test-driven development approach. The implementation should be properly typed and documented with docstrings.

The YAML output should follow Ansible best practices and be compatible with the Ansible CLI.
```

### Prompt 2.4: ansible_runner Integration

```
Now I need to implement the integration with ansible_runner for the Ansible Development Kit (ADK) component of the EPCOT project. This will allow the ADK to execute Ansible playbooks programmatically.

Based on the previously implemented BaseTask and Playbook classes, please implement:
1. Methods for converting Task objects to ansible_runner dictionaries
2. Methods for converting Playbook objects to ansible_runner dictionaries
3. Validation during the conversion process to ensure the generated dictionaries are valid
4. Utility functions for executing the playbooks using ansible_runner

Include comprehensive unit tests for all functionality, following the test-driven development approach. The implementation should be properly typed and documented with docstrings.

The ansible_runner integration should follow best practices and be compatible with the latest version of ansible_runner.
```

### Prompt 2.5: Basic Task Implementations

```
Now I need to implement the basic task classes for the Ansible Development Kit (ADK) component of the EPCOT project. These classes will represent specific Ansible modules.

Based on the previously implemented BaseTask class, please implement:
1. FileTask class for the ansible.builtin.file module
   - Properties for path, state, mode, owner, group, etc.
   - Validation methods specific to file tasks
2. TemplateTask class for the ansible.builtin.template module
   - Properties for src, dest, mode, owner, group, etc.
   - Validation methods specific to template tasks
3. ServiceTask class for the ansible.builtin.service module
   - Properties for name, state, enabled, etc.
   - Validation methods specific to service tasks

Include comprehensive unit tests for all functionality, following the test-driven development approach. The implementation should be properly typed and documented with docstrings.

The task implementations should follow Ansible best practices and support all required parameters for each module.
```

### Prompt 2.6: User and Group Task Implementations

```
Now I need to implement the user and group task classes for the Ansible Development Kit (ADK) component of the EPCOT project. These classes will represent the ansible.builtin.user and ansible.builtin.group modules.

Based on the previously implemented BaseTask class, please implement:
1. UserTask class for the ansible.builtin.user module
   - Properties for name, state, shell, home, groups, etc.
   - Validation methods specific to user tasks
2. GroupTask class for the ansible.builtin.group module
   - Properties for name, state, gid, etc.
   - Validation methods specific to group tasks
3. Utility functions for associating users with groups

Include comprehensive unit tests for all functionality, following the test-driven development approach. The implementation should be properly typed and documented with docstrings.

The task implementations should follow Ansible best practices and support all required parameters for each module.
```

### Prompt 2.7: Package Management Task Implementations

```
Now I need to implement the package management task classes for the Ansible Development Kit (ADK) component of the EPCOT project. These classes will represent various package management modules.

Based on the previously implemented BaseTask class, please implement:
1. AptTask class for the ansible.builtin.apt module
   - Properties for name, state, update_cache, etc.
   - Validation methods specific to apt tasks
2. PipTask class for the ansible.builtin.pip module
   - Properties for name, state, version, etc.
   - Validation methods specific to pip tasks
3. AptKeyTask class for the ansible.builtin.apt_key module
   - Properties for url, state, etc.
   - Validation methods specific to apt_key tasks
4. AptRepositoryTask class for the ansible.builtin.apt_repository module
   - Properties for repo, state, etc.
   - Validation methods specific to apt_repository tasks

Include comprehensive unit tests for all functionality, following the test-driven development approach. The implementation should be properly typed and documented with docstrings.

The task implementations should follow Ansible best practices and support all required parameters for each module.
```

### Prompt 2.8: Docker Task Implementations

```
Now I need to implement the Docker task classes for the Ansible Development Kit (ADK) component of the EPCOT project. These classes will represent Docker-related Ansible modules.

Based on the previously implemented BaseTask class, please implement:
1. DockerComposeTask class for the community.docker.docker_compose_v2 module
   - Properties for project_src, files, state, etc.
   - Validation methods specific to docker_compose tasks
2. DockerPruneTask class for the community.docker.docker_prune module
   - Properties for containers, images, networks, volumes, etc.
   - Validation methods specific to docker_prune tasks

Include comprehensive unit tests for all functionality, following the test-driven development approach. The implementation should be properly typed and documented with docstrings.

The task implementations should follow Ansible best practices and support all required parameters for each module.
```

### Prompt 2.9: Network Task Implementations

```
Now I need to implement the network task classes for the Ansible Development Kit (ADK) component of the EPCOT project. These classes will represent network-related Ansible modules.

Based on the previously implemented BaseTask class, please implement:
1. IPTablesTask class for the ansible.builtin.iptables module
   - Properties for chain, table, rule, state, etc.
   - Validation methods specific to iptables tasks

Include comprehensive unit tests for all functionality, following the test-driven development approach. The implementation should be properly typed and documented with docstrings.

The task implementations should follow Ansible best practices and support all required parameters for each module.
```

## Phase 3: Client Core

### Prompt 3.1: YAML Parsing

```
Now I need to implement the YAML parsing functionality for the client component of the EPCOT project. This will be used to load and validate figment configuration files.

Please implement:
1. Functions for loading YAML files
2. Basic validation of the YAML structure
3. Error reporting for invalid YAML files
4. Support for including other YAML files

Include comprehensive unit tests for all functionality, following the test-driven development approach. The implementation should be properly typed and documented with docstrings.

The YAML parsing should follow best practices and be compatible with the PyYAML library.
```

### Prompt 3.2: Variable Substitution

```
Now I need to implement the variable substitution system for the client component of the EPCOT project. This will be used to replace variable references in figment configuration files.

Based on the previously implemented YAML parsing functionality, please implement:
1. Functions for parsing variable references in the format `{{ $INPUT.variable_name }}`, `{{ $VAR.variable_name }}`, and `{{ $figment.PROVIDES.variable_name }}`
2. Functions for substituting variable references with their values
3. Validation for variable references to ensure they are valid
4. Error reporting for invalid variable references

Include comprehensive unit tests for all functionality, following the test-driven development approach. The implementation should be properly typed and documented with docstrings.

The variable substitution system should follow the requirements specified in the project documentation.
```

### Prompt 3.3: Figment Base Class

```
Now I need to implement the base Figment class for the client component of the EPCOT project. This class will be the foundation for all figments in the system.

Based on the previously defined interfaces and the YAML parsing and variable substitution functionality, please implement:
1. An abstract BaseFigment class that implements the Figment interface
2. Common figment properties and methods:
   - name
   - configuration
   - provides
   - dependencies
3. Methods for loading figment configuration from YAML files
4. Methods for validating figment configuration
5. Methods for resolving dependencies between figments

Include comprehensive unit tests for all functionality, following the test-driven development approach. The implementation should be properly typed and documented with docstrings.

The BaseFigment class should follow the requirements specified in the project documentation and be designed to be extended by specific figment implementations.
```

### Prompt 3.4: Task Generation

```
Now I need to implement the task generation functionality for the client component of the EPCOT project. This will convert figment configurations into Ansible tasks.

Based on the previously implemented BaseFigment class and the ADK components, please implement:
1. Methods for converting figment data to ADK Task objects
2. Methods for aggregating tasks from multiple figments
3. Validation during task generation to ensure the generated tasks are valid
4. Error reporting for invalid task generation

Include comprehensive unit tests for all functionality, following the test-driven development approach. The implementation should be properly typed and documented with docstrings.

The task generation should follow the requirements specified in the project documentation and be designed to work with the ADK components.
```

### Prompt 3.5: Task Ordering

```
Now I need to implement the task ordering functionality for the client component of the EPCOT project. This will ensure that tasks are executed in the correct order.

Based on the previously implemented task generation functionality, please implement:
1. Methods for ordering tasks based on the requirements specified in the project documentation
2. Validation for task dependencies to ensure there are no circular dependencies
3. Task deduplication to ensure that identical tasks are only executed once
4. Error reporting for invalid task ordering

Include comprehensive unit tests for all functionality, following the test-driven development approach. The implementation should be properly typed and documented with docstrings.

The task ordering should follow the requirements specified in the project documentation and ensure that tasks are executed in the correct order.
```

## Phase 4: Figment Implementations

### Prompt 4.1: Basic Figments

```
Now I need to implement the basic figments for the client component of the EPCOT project. These figments will handle user, group, file, and directory management.

Based on the previously implemented BaseFigment class, please implement:
1. UserFigment class for managing users
   - Methods for generating UserTask objects
   - Configuration validation specific to user management
2. GroupFigment class for managing groups
   - Methods for generating GroupTask objects
   - Configuration validation specific to group management
3. FileFigment class for managing files
   - Methods for generating FileTask objects
   - Configuration validation specific to file management
4. DirectoryFigment class for managing directories
   - Methods for generating FileTask objects with directory-specific parameters
   - Configuration validation specific to directory management

Include comprehensive unit tests for all functionality, following the test-driven development approach. The implementation should be properly typed and documented with docstrings.

The figment implementations should follow the requirements specified in the project documentation and be designed to work with the ADK components.
```

### Prompt 4.2: Package Management Figments

```
Now I need to implement the package management figments for the client component of the EPCOT project. These figments will handle apt packages, pip packages, and repositories.

Based on the previously implemented BaseFigment class, please implement:
1. AptFigment class for managing apt packages
   - Methods for generating AptTask objects
   - Configuration validation specific to apt package management
2. PipFigment class for managing pip packages
   - Methods for generating PipTask objects
   - Configuration validation specific to pip package management
3. RepositoryFigment class for managing repositories
   - Methods for generating AptRepositoryTask and AptKeyTask objects
   - Configuration validation specific to repository management

Include comprehensive unit tests for all functionality, following the test-driven development approach. The implementation should be properly typed and documented with docstrings.

The figment implementations should follow the requirements specified in the project documentation and be designed to work with the ADK components.
```

### Prompt 4.3: Service Figments

```
Now I need to implement the service figments for the client component of the EPCOT project. These figments will handle service management.

Based on the previously implemented BaseFigment class, please implement:
1. ServiceFigment class for managing services
   - Methods for generating ServiceTask objects
   - Configuration validation specific to service management
2. Integration with systemd for service management
   - Methods for generating systemd-specific ServiceTask objects
   - Configuration validation specific to systemd service management

Include comprehensive unit tests for all functionality, following the test-driven development approach. The implementation should be properly typed and documented with docstrings.

The figment implementations should follow the requirements specified in the project documentation and be designed to work with the ADK components.
```

### Prompt 4.4: Docker Figments

```
Now I need to implement the Docker figments for the client component of the EPCOT project. These figments will handle Docker container and network management.

Based on the previously implemented BaseFigment class, please implement:
1. DockerFigment class for managing Docker containers
   - Methods for generating DockerComposeTask objects
   - Configuration validation specific to Docker container management
2. DockerNetworkFigment class for managing Docker networks
   - Methods for generating Docker network-specific tasks
   - Configuration validation specific to Docker network management

Include comprehensive unit tests for all functionality, following the test-driven development approach. The implementation should be properly typed and documented with docstrings.

The figment implementations should follow the requirements specified in the project documentation and be designed to work with the ADK components.
```

### Prompt 4.5: Network Figments

```
Now I need to implement the network figments for the client component of the EPCOT project. These figments will handle network configuration.

Based on the previously implemented BaseFigment class, please implement:
1. IPTablesFigment class for managing iptables rules
   - Methods for generating IPTablesTask objects
   - Configuration validation specific to iptables rule management
2. NetworkFigment class for managing network configuration
   - Methods for generating network configuration-specific tasks
   - Configuration validation specific to network configuration

Include comprehensive unit tests for all functionality, following the test-driven development approach. The implementation should be properly typed and documented with docstrings.

The figment implementations should follow the requirements specified in the project documentation and be designed to work with the ADK components.
```

### Prompt 4.6: Provider Figments

```
Now I need to implement the provider figments for the client component of the EPCOT project. These figments will provide services to other figments.

Based on the previously implemented BaseFigment class, please implement:
1. UdevFigment class for managing udev rules
   - Methods for generating udev rule-specific tasks
   - Configuration validation specific to udev rule management
   - Methods for collecting udev configurations from other figments
2. ReverseProxyFigment class for managing reverse proxy configurations
   - Methods for generating reverse proxy-specific tasks
   - Configuration validation specific to reverse proxy management
   - Methods for collecting reverse proxy configurations from other figments
3. IntrusionDetectionFigment class for managing intrusion detection
   - Methods for generating intrusion detection-specific tasks
   - Configuration validation specific to intrusion detection management
   - Methods for collecting intrusion detection configurations from other figments

Include comprehensive unit tests for all functionality, following the test-driven development approach. The implementation should be properly typed and documented with docstrings.

The figment implementations should follow the requirements specified in the project documentation and be designed to work with the ADK components.
```

### Prompt 4.7.1: Media Server Figment

```
Now I need to implement the Media Server figment for the client component of the EPCOT project. This figment will handle media server configuration.

Based on the previously implemented BaseFigment class, please implement:
1. MediaServerFigment class for managing media server configuration
   - Methods for generating media server-specific tasks
   - Configuration validation specific to media server management
   - Integration with Docker for container management
   - Integration with reverse proxy for external access

Include comprehensive unit tests for all functionality, following the test-driven development approach. The implementation should be properly typed and documented with docstrings.

The figment implementation should follow the requirements specified in the project documentation and be designed to work with the ADK components.
```

### Prompt 4.7.2: Transcode Figment

```
Now I need to implement the Transcode figment for the client component of the EPCOT project. This figment will handle media transcoding.

Based on the previously implemented BaseFigment class, please implement:
1. TranscodeFigment class for managing media transcoding
   - Methods for generating transcode-specific tasks
   - Configuration validation specific to transcode management
   - Integration with Docker for container management
   - Integration with media server for content access

Include comprehensive unit tests for all functionality, following the test-driven development approach. The implementation should be properly typed and documented with docstrings.

The figment implementation should follow the requirements specified in the project documentation and be designed to work with the ADK components.
```

### Prompt 4.7.3: Tunnel Figment

```
Now I need to implement the Tunnel figment for the client component of the EPCOT project. This figment will handle secure tunneling.

Based on the previously implemented BaseFigment class, please implement:
1. TunnelFigment class for managing secure tunneling
   - Methods for generating tunnel-specific tasks
   - Configuration validation specific to tunnel management
   - Integration with Docker for container management
   - Integration with reverse proxy for external access

Include comprehensive unit tests for all functionality, following the test-driven development approach. The implementation should be properly typed and documented with docstrings.

The figment implementation should follow the requirements specified in the project documentation and be designed to work with the ADK components.
```

### Prompt 4.7.4: Other Specialized Figments

```
Now I need to implement the remaining specialized figments for the client component of the EPCOT project. These figments will handle various specialized configurations.

Based on the previously implemented BaseFigment class, please implement:
1. BackupFigment class for managing backups
   - Methods for generating backup-specific tasks
   - Configuration validation specific to backup management
2. CertificatesFigment class for managing SSL certificates
   - Methods for generating certificate-specific tasks
   - Configuration validation specific to certificate management
3. DHCPFigment class for managing DHCP
   - Methods for generating DHCP-specific tasks
   - Configuration validation specific to DHCP management
4. DNSFigment class for managing DNS
   - Methods for generating DNS-specific tasks
   - Configuration validation specific to DNS management
5. HomeAutomationFigment class for managing home automation
   - Methods for generating home automation-specific tasks
   - Configuration validation specific to home automation management
6. SecurityFigment class for managing security
   - Methods for generating security-specific tasks
   - Configuration validation specific to security management
7. ShellFigment class for managing shell configurations
   - Methods for generating shell-specific tasks
   - Configuration validation specific to shell management
8. UnifiFigment class for managing Unifi equipment
   - Methods for generating Unifi-specific tasks
   - Configuration validation specific to Unifi management

Include comprehensive unit tests for all functionality, following the test-driven development approach. The implementation should be properly typed and documented with docstrings.

The figment implementations should follow the requirements specified in the project documentation and be designed to work with the ADK components.
```

## Phase 5: Integration and Testing

### Prompt 5.1: End-to-End Testing

```
Now I need to implement end-to-end testing for the EPCOT project. This will test the complete system with sample configurations.

Please implement:
1. End-to-end test cases that:
   - Load sample figment configurations
   - Generate tasks from the configurations
   - Create a playbook from the tasks
   - Validate the playbook
   - Convert the playbook to YAML
   - Validate the YAML
2. Integration tests for all components
3. Test fixtures for end-to-end testing

Include comprehensive documentation for the test cases, following the test-driven development approach. The implementation should be properly typed and documented with docstrings.

The end-to-end tests should follow best practices and be designed to catch integration issues between components.
```

### Prompt 5.2: Schema Validation

```
Now I need to implement schema validation for the EPCOT project. This will validate the structure of figment configuration files.

Please implement:
1. Schema definitions for all figment configuration files
2. Validation functions for checking figment configurations against the schemas
3. Error reporting for schema validation failures
4. Integration with the figment loading process

Include comprehensive unit tests for all functionality, following the test-driven development approach. The implementation should be properly typed and documented with docstrings.

The schema validation should follow the requirements specified in the project documentation and be designed to catch configuration errors early.
```

### Prompt 5.3: Error Reporting

```
Now I need to enhance the error reporting throughout the EPCOT project. This will provide detailed error messages for various failure scenarios.

Please implement:
1. Enhanced error reporting for:
   - YAML parsing errors
   - Schema validation errors
   - Variable substitution errors
   - Task generation errors
   - Playbook generation errors
2. Detailed error messages that include:
   - Error location (figment name and field path)
   - Description of the validation failure
   - Suggested fix when applicable
3. Error handling and recovery mechanisms

Include comprehensive unit tests for all functionality, following the test-driven development approach. The implementation should be properly typed and documented with docstrings.

The error reporting should follow the requirements specified in the project documentation and be designed to help users diagnose and fix issues.
```

### Prompt 5.4: Documentation

```
Now I need to complete the documentation for the EPCOT project. This will include API documentation, user documentation, and developer documentation.

Please implement:
1. Complete API documentation using Sphinx
   - Document all classes, methods, and functions
   - Include type information
   - Include examples
2. User documentation
   - Installation instructions
   - Configuration guide
   - Usage examples
3. Developer documentation
   - Architecture overview
   - Extension guide
   - Contribution guide
4. Examples and tutorials
   - Basic usage examples
   - Advanced usage examples
   - Troubleshooting guide

The documentation should follow best practices and be designed to help users and developers understand and use the system.
```

## Phase 6: Integration and Wiring

### Prompt 6.1: Main Application

```
Now I need to implement the main application for the EPCOT project. This will tie all the components together and provide a command-line interface.

Please implement:
1. A main application class that:
   - Loads figment configurations
   - Generates tasks from the configurations
   - Creates a playbook from the tasks
   - Executes the playbook using ansible_runner
   - Reports results
2. A command-line interface for the application
3. Configuration options for the application

Include comprehensive unit tests for all functionality, following the test-driven development approach. The implementation should be properly typed and documented with docstrings.

The main application should follow the requirements specified in the project documentation and be designed to be easy to use.
```

### Prompt 6.2: Final Integration

```
Now I need to perform the final integration for the EPCOT project. This will ensure that all components work together correctly.

Please implement:
1. Integration between all components
2. Final validation of the system
3. Performance optimizations
4. Final documentation updates

Include comprehensive integration tests for all functionality, following the test-driven development approach. The implementation should be properly typed and documented with docstrings.

The final integration should follow the requirements specified in the project documentation and ensure that the system works correctly as a whole.
```