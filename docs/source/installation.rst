Installation
===========

Prerequisites
------------

* Python 3.12.3
* Poetry (for dependency management)

Installing from Source
---------------------

Clone the repository:

.. code-block:: bash

    git clone https://github.com/yourusername/epcot.git
    cd epcot

Install using Poetry:

.. code-block:: bash

    poetry install

This will create a virtual environment and install all dependencies.

Development Installation
-----------------------

For development, you'll want to install the development dependencies as well:

.. code-block:: bash

    poetry install --with dev

This will install additional tools like:

* Black (code formatter)
* Flake8 (linter)
* Pytest (testing framework)
* Sphinx (documentation generator)
* Mypy (type checker)