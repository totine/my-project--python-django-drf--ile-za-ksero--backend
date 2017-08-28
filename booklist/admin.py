from django.contrib import admin
from booklist.models import Author, Book, BookAuthor

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BookAuthor)
