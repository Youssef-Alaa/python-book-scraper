import re
import logging
from bs4 import BeautifulSoup

from locators.books_page import AllBooksLocator
from parsers.book import BookParser

logger = logging.getLogger('scraping.books_page')

class BooksPage:
    def __init__(self, page):
        self.soup = BeautifulSoup(page, 'html.parser')

    @property
    def books(self):
        logger.debug(f'Finding all books in the page using `{AllBooksLocator.BOOKS}`')
        return [BookParser(e) for e in self.soup.select(AllBooksLocator.BOOKS)]

    @property
    def page_count(self):
        content = self.soup.select_one(AllBooksLocator.PAGER).string
        logger.info(f'Found number of catalogue pages available: `{content}`')
        pattern = 'Page [0-9]+ of ([0-9]+)'
        matcher = re.search(pattern, content)
        pages = int(matcher.group(1))
        logger.info(f'Extracted number of pages as integer: `{pages}`.')
        return pages