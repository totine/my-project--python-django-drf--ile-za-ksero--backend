from django.shortcuts import render, HttpResponse

from booklist.models import XeroBook


def home(request):
    books = XeroBook.objects.all()
    print(books[0].book.author_set.all(), books[0].book.number_of_pages_id, books[0].book)
    data = {"books": books}
    return render(request, 'home.html', context=data)

