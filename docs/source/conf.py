# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))


project = 'yipao'
copyright = '2024, FacilPost'
author = 'Factral, Daniel'
version  = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]
autosummary_generate = True  # Turn on sphinx.ext.autosummary

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme_options = {
    "logo_light": "_static/logo.png",
    "logo_dark": "_static/logo.png"
}
html_title = "Yipao"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output





html_theme = "sphinxawesome_theme"
extensions += ["sphinxawesome_theme.highlighting"]
html_static_path = ['_static']
