# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os 
import sys 

sys.path.insert(0,os.path.abspath('../../atvm'))

project = 'ATVM documentation'
copyright = '2024, Riwa Hachem Reda, Wahel El Mazzouji, Lucien Duigo, Lamia Oulebsir'
author = 'Riwa Hachem Reda, Wahel El Mazzouji, Lucien Duigo, Lamia Oulebsir'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.todo","sphinx.ext.viewcode","sphinx.ext.autodoc","sphinx.ext.napoleon","sphinx.ext.githubpages"]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_baseurl = "https://riwahachem.github.io/Projet_HAX712X/"

language = 'fr'

autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private-members': True,
    'show-inheritance': True,
    'inherited-members': True
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_show_sourcelink = False  # Pour GitHub Pages
html_static_path = []

autodoc_member_order = 'groupwise'
