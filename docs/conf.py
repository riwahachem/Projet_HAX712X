# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sphinx_rtd_theme
import os
import sys 

sys.path.insert(0,os.path.abspath(".."))

project = 'ATVM'
copyright = '2024, Riwa Hachem Reda, Wahel El Mazzouji, Lucien Duigou, Lamia Oulebsir'
author = 'Riwa Hachem Reda, Wahel El Mazzouji, Lucien Duigou, Lamia Oulebsir'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.todo","sphinx.ext.viewcode","sphinx.ext.autodoc"]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'fr'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
