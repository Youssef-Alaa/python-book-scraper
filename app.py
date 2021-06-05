import requests
import logging

from pages.books_page import BooksPage

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    level=logging.DEBUG,
                    filename='logs.log')
logger = logging.getLogger('scraping')

logger.info('Loading books list.')

logger.info('Requesting http://books.toscrape.com')
page_content = requests.get('http://books.toscrape.com').content

page = BooksPage(page_content)
books_list = []

for page_num in range(page.page_count):
    url = f'http://books.toscrape.com/catalogue/page-{page_num+1}.html'
    page_content = requests.get(url).content
    logger.debug('Creating AllBooksPage from page content.')

    page = BooksPage(page_content)
    books_list.extend(page.books)

# books_list = _books_list