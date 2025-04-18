# General Requirements
# EPCOT Schema Validation Requirements

## 1. Basic Schema Requirements
- Each figment schema MUST be a valid YAML document
- All template variables MUST follow the format `{{ $INPUT.variable_name }}` or `{{ $VAR.variable_name }}`

## 2. Top-Level Sections
The following sections are optional but MUST follow defined structure when present:
- `vars`: Key-value pairs for internal figment variables
- `directories`: List of directory configurations
- `files`: List of file configurations
- `docker`: Docker-related configurations
- `provides`: Values this figment makes available to other figments

## 3. Docker Service Validation
- Under `docker.services`:
  - MUST be a flat list (no nested `services` keys)
  - Each service MAY include:
    - `config_dir`
    - `volumes`
    - `networks`
    - `environment`
    - `capabilities`
    - Other standard Docker service configurations

## 4. Dependencies and References
- Values referenced from other figments MUST:
  - Reference an existing figment
  - Reference a value defined in that figment's `provides` section
- Circular dependencies between figments:
  - MUST be allowed during validation
  - MAY result in runtime errors during Ansible playbook execution
  - No validation errors should be raised for circular references
  - Users are responsible for ensuring their circular references are resolvable or for handling resulting errors appropriately

## 5. Error Reporting
Validation errors MUST include:
- Error location (figment name and field path)
- Description of the validation failure
- Suggested fix when applicable

## 6. Volume References
- Volume names referenced in `volumes` sections MUST be:
  - Defined in the same figment's `directories` section, OR
  - Provided by another figment through its `provides` section
 * This project will be released under the MIT license.
    * All dependencies must be compatible with the MIT license.
 * This project will be built using Python 3.12.3
 * Dependencies of this project will be managed using Poetry.
 * All code must be typed.
 * All code must be formatted using Black.
 * All code must be linted using Flake8.
 * All code must be documented using Sphinx.
 * All code must be thoroughly tested using Pytest.
 * All tests and linting rules must pass before a pull request can be merged.
   * GitHub Actions will be used to enforce this.

# Scope

There are two parts to this project:

 * An Ansible Development Kit (ADK) that will allow ansible tasks to be modeled programmatically.
 * A client of the ADK.

# Ansible Development Kit (ADK)

 * It must be possible to create a `Task` object for each of the following Ansible modules:
    * `ansible.builtin.user`
    * `ansible.builtin.group`
    * `ansible.buildin.apt_key`
    * `ansible.builtin.apt_repository`
    * `ansible.builtin.apt`
    * `ansible.builtin.service`
    * `ansible.builtin.file`
    * `ansible.builtin.template`
    * `ansible.builtin.pip`
    * `community.docker.docker_compose_v2`
    * `community.docker.docker_prune`
    * `ansible.builtin.iptables`
 * Only parameters of these modules that are required for the client will be modeled at this time.
 * It must be possible to create a `Playbook` object that these tasks can be added to.
 * It must be possible to convert a `Playbook` to a dictionary that can be provided to `ansible_runner.run`.
 * It must be possible to output the `Playbook` to a YAML file that can be used by the Ansible CLI.
 * The ADK must be implemented in such a way that it can be extracted to a separate library that can be used by other projects.

# Client Requirements

 * The client will define several "Figments".
 * All figments are capable of providing lists of:
   * `File` tasks
   * `Template` tasks
   * `Service` tasks
   * Other tasks
   * Directories
   * Debian repositories
   * `apt Keys` tasks
   * `apt Packages` tasks
   * `apt PPAs` tasks
   * Users
   * Groups
   * PIP modules
 * For the lists that don't return ADK tasks, the client will be responsible for converting them to ADK tasks.
   * This will allow the minimum number of tasks necessary to be created, for example, there should only be 1 task for installing all apt packages.
 * The default behaviour of each figment is to read the values it provides from <figment name>/figment.yaml.
 * Individual figments can override this behaviour by using a decorator.
 * The following figments are necessary:
   * backup
   * certificates
   * dhcp
   * dns
   * docker
   * intrusion-detection
   * home-automation
   * iptables
   * media-rip
   * media-server
   * reverse-proxy
   * security
   * shell
   * transcode
   * tunnel
   * udev
   * unifi
 * Some figments are udev, reverse_proxy, iptable, docker or intrusion_detection providers
   * The additional configuration needed by these providers will also be located in <figment name>/figment.yaml.
   * The udev, reverse_proxy, iptable, docker and intrusion_detection figments will visit all other figments to load the necessary configuration. 
 * When loading figment.yaml files, values contained within {{ }} should be replaced by the name of an ansible variable.
   * When the value inside the {{ }} begins with:
     * "$INPUT.", the "$INPUT." should be replaced with "__<figment name>__input__".  An ansible variable of the same name should be created from a constructor argument to the figment with the same name.  For example, in the dhcp figment, {{ $INPUT.port }} should be replaced with {{ __dhcp__input__port }} and the ansible variable __dhcp__input__port should be set to the port parameter to the dhcp figment constructor.
     * "$VAR.", the "$VAR." should be replaced with "__<figment name>__var__".  An ansible variable of the same name should be created based on the value of the same name found in the vars section of <figment name>/figment.yaml.  For example, in the dhcp figment, {{ $VAR.port }} should be replaced with {{ __dhcp__var__port }} and the ansible variable __dhcp__var__port should be set to the vars.port parameter in dhcp/figment.yaml.
     * Anything else, a parse error should be raised.
 * There will be an epcot.yaml file at the top of the directory structure
   * It defines what figments will be loaded
   * It includes the input parameters to that figment
     * If an input parameter is not provided, a default value will be used
     * Values contained within {{ }} should be replaced by the name of an ansible variable.
       * When the value inside the {{ }} begins with:
         * "$<figment name>.PROVIDES.", the "$<figment name>.PROVIDES." should be replaced with "__<figment name>__provides__".  An ansible variable of the same name should be created based on the value of the same name found in the provides section of <figment name>/figment.yaml.  For example {{ $dns.PROVIDES.port }} should be replaced with {{ __dns__provides__port }} and the ansible variable __dns_provides__port should be set to the provies.port parameter in dns/figment.yaml.
         * Anything else, a parse error should be raised.
 * After all figments have been loaded, and all figments have visited all other figments, an ADK `Playbook` should be generated that contains tasks in the following order:
   * Create users
   * Create groups
   * Add users to groups
   * Set user shell
   * Add apt keys
   * Add apt PPAs
   * Add deb repositories
   * Install apt packages
   * Upgrade apt packages
   * Disable services if necessary
   * Custom tasks from the udev figment
   * Custom tasks from the iptables figment
   * Create directories
   * Create files and templates
   * Update pip
   * Install python modules
   * Flush handlers
   * Custom tasks from the docker figment
   * Start services on boot
   * Remove unused apt packages