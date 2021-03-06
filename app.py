import asyncio
import aiohttp
import async_timeout
import time
import requests
import logging

from pages.books_page import BooksPage

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    level=logging.DEBUG,
                    filename='logs.log')
logger = logging.getLogger('scraping')

loop = asyncio.get_event_loop()

logger.info('Loading books list.')

logger.info('Requesting http://books.toscrape.com')
page_content = requests.get('http://books.toscrape.com').content

page = BooksPage(page_content)
books_list = []

async def fetch_page(session, url):
    page_start = time.time()
    logger.info(f'Requesting {url}')
    async with session.get(url) as response:
        print(f'{url} took {time.time() - page_start}')
        return await response.text()


async def get_multiple_pages(loop, *urls):
    tasks = []
    async with aiohttp.ClientSession(loop=loop) as session:
        for url in urls:
            tasks.append(fetch_page(session, url))
        return await asyncio.gather(*tasks)

urls = [f'http://books.toscrape.com/catalogue/page-{page_num+1}.html' for page_num in range(page.page_count)]
start = time.time()
pages = loop.run_until_complete(get_multiple_pages(loop, *urls))
print(f'Total page requests took {time.time() - start}')

for page_content in pages:
    logger.debug('Creating AllBooksPage from page content.')
    page = BooksPage(page_content)
    books_list.extend(page.books)

# books_list = _books_list