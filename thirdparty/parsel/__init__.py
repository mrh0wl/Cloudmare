"""
Parsel lets you extract text from XML/HTML documents using XPath
or CSS selectors
"""

__author__ = 'Scrapy project'
__email__ = 'info@scrapy.org'
__version__ = '1.6.0'

from thirdparty.parsel.selector import Selector, SelectorList  # NOQA
from thirdparty.parsel.csstranslator import css2xpath  # NOQA
from thirdparty.parsel import xpathfuncs # NOQA

xpathfuncs.setup()
