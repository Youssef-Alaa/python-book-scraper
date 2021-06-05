import re
from bs4 import BeautifulSoup

from locators.books_page import AllBooksLocator
from parsers.book import BookParser


class BooksPage:
    def __init__(self, page):
        self.soup = BeautifulSoup(page, 'html.parser')

    @property
    def books(self):
        return [BookParser(e) for e in self.soup.select(AllBooksLocator.BOOKS)]

    @property
    def page_count(self):
        content = self.soup.select_one(AllBooksLocator.PAGER).string
        pattern = 'Page [0-9]+ of ([0-9]+)'
        matcher = re.search(pattern, content)
        pages = int(matcher.group(1))
        return pages