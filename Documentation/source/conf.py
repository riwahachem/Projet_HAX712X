# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
#sys.path.insert(0, os.path.abspath('C:/Users/welma/HAX712X_WAHEL/Projet_HAX712X/data'))
sys.path.insert(0, os.path.abspath('../data'))


project = 'ATVM'
copyright = '2024, Riwa Hachem Reda, Wahel El Mazzouji, Lucien Duigou, Lamia Oulebsir'
author = 'Riwa Hachem Reda, Wahel El Mazzouji, Lucien Duigou, Lamia Oulebsir'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',        
    'sphinx.ext.napoleon',       
    'sphinx_autodoc_typehints' 
]


templates_path = ['_templates']
exclude_patterns = []

language = 'fr'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
