import requests

from pages.books_page import BooksPage

page_content = requests.get('http://books.toscrape.com/').content
page = BooksPage(page_content)

print("hi i am working")
books = page.books

for book in books:
    print(book)