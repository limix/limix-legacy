from __future__ import unicode_literals

try:
    import limix
    version = limix_legacy.__version__
except ImportError:
    version = 'unknown'

extensions = [
    'sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax', 'sphinx.ext.viewcode', 'sphinx.ext.napoleon'
]
napoleon_google_docstring = True
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'limix'
copyright = '2017, Oliver Stegle'
author = 'Oliver Stegle'
release = version
language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
todo_include_todos = False
html_theme = 'default'
htmlhelp_basename = 'limixdoc'
man_pages = [(master_doc, 'limix', 'limix Documentation', [author], 1)]
texinfo_documents = [
    (master_doc, 'limix', 'limix Documentation', author, 'limix',
     'A flexible and fast mixed model toolbox.', 'Miscellaneous'),
]
intersphinx_mapping = {
    'https://docs.python.org/': None,
    'numpy': ('http://docs.scipy.org/doc/numpy/', None)
}
