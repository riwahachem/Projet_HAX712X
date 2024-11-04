# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ATVM'
copyright = '2024, Riwa Hachem Reda, Wahel El Mazzouji, Lucien Duigou, Lamia Oulebsir'
author = 'Riwa Hachem Reda, Wahel El Mazzouji, Lucien Duigou, Lamia Oulebsir'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'fr'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

import os
import sys
sys.path.insert(0, os.path.abspath('../atvm'))


html_theme = 'alabaster'
html_static_path = ['_static']
