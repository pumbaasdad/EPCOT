# EPCOT - Experimental Prototype Community of Tomorrow

[![CI](https://github.com/yourusername/EPCOT/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/EPCOT/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12.3](https://img.shields.io/badge/python-3.12.3-blue.svg)](https://www.python.org/downloads/release/python-3123/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

EPCOT is a system for managing various components (figments) of a home automation and media server setup.

## Project Requirements

This project adheres to the following requirements:

- Released under the MIT license
- Built using Python 3.12.3
- Dependencies managed using Poetry
- All code is typed with MyPy
- All code is formatted using Black
- All code is linted using Flake8
- All code is documented using Sphinx
- All code is thoroughly tested using Pytest
- All tests and linting rules must pass before a pull request can be merged (enforced by GitHub Actions)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/EPCOT.git
cd EPCOT

# Install Poetry if you don't have it
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install
```

## Development

### Setting up the development environment

```bash
# Create and activate the virtual environment
poetry shell

# Install development dependencies
poetry install
```

### Running tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src
```

### Code formatting and linting

```bash
# Format code with Black
black .

# Check code with Flake8
flake8

# Check typing with MyPy
mypy src tests
```

### Building documentation

```bash
# Build Sphinx documentation
cd docs
sphinx-build -b html source build/html
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
