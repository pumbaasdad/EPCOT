"""Sphinx configuration for EPCOT documentation."""

import os
import sys
from datetime import datetime

# Add the project source directory to the path
sys.path.insert(0, os.path.abspath("../../src"))

# Project information
project = "EPCOT"
copyright = f"{datetime.now().year}, EPCOT Contributors"
author = "EPCOT Contributors"

# Import the project to get the version
import epcot  # noqa: E402

version = epcot.__version__
release = version

# General configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
]

templates_path = ["_templates"]
exclude_patterns = []

# HTML output options
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# Todo settings
todo_include_todos = True
