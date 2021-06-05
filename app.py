import requests

from pages.books_page import BooksPage

page_content = requests.get('http://books.toscrape.com').content

page = BooksPage(page_content)
books_list = []

for page_num in range(page.page_count):
    url = f'http://books.toscrape.com/catalogue/page-{page_num+1}.html'
    page_content = requests.get(url).content
    page = BooksPage(page_content)
    books = page.books
    books_list.append(books)