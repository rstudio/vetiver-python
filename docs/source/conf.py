import os
import sys
import re
from vetiver import __version__ as version

sys.path.insert(0, os.path.abspath("."))


# -- Project information -----------------------------------------------------

project = "vetiver"
copyright = "2022, RStudio"
author = "Isabel Zimmerman"

# The full version, including alpha/beta/rc tags
# Do not use the 0.0 version created by setuptools_scm when the package
# is cloned too shallow to pickup
p = re.compile(r"^0\.0\.post\d+\+g")
if p.match(version):
    commit = p.sub("", version)
    version = f"Commit: {commit}"

release = version

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.githubpages",
    "sphinx.ext.autodoc",
    "myst_parser",
]
# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_book_theme"

html_theme_options = {
    "repository_url": "https://github.com/tidymodels/vetiver-python",
    "use_repository_button": True,
    "use_issues_button": True,
    "use_edit_page_button": True,
    "home_page_in_toc": True,
}

source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}
myst_heading_anchors = 2

html_logo = "../figures/logo.png"
html_favicon = "../figures/logo.png"


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []
