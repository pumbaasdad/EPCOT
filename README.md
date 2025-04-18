# EPCOT

EPCOT (Experimental Prototype Configuration of Tomorrow) is a system for managing infrastructure using Ansible.

## Overview

EPCOT provides a programmatic interface for creating and managing Ansible tasks and playbooks. It allows for modular infrastructure management through "Figments" - reusable components that provide various system configurations.

## Features

- Ansible Development Kit (ADK) for programmatic creation of Ansible tasks and playbooks
- Modular infrastructure management through Figments
- Type-safe Python API with comprehensive type hints
- Test-driven development approach

## Requirements

- Python 3.12.3
- Poetry for dependency management

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/epcot.git
cd epcot

# Install dependencies using Poetry
poetry install
```

## Development

This project uses:
- Black for code formatting
- Flake8 for linting
- Pytest for testing
- Mypy for type checking
- Sphinx for documentation

### Setup Development Environment

```bash
# Install development dependencies
poetry install --with dev

# Run tests
poetry run pytest

# Run linting
poetry run flake8

# Run type checking
poetry run mypy src/epcot

# Format code
poetry run black src tests
```

## Documentation

Documentation is built using Sphinx and can be found in the `docs/` directory.

To build the documentation:

```bash
cd docs
poetry run make html
```

Then open `docs/_build/html/index.html` in your browser.

## License

[MIT License](LICENSE)