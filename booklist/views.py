from django.shortcuts import render, HttpResponse

from booklist.models import Book


def home(request):
    books = Book.objects.all()
    data = {"books": books}
    return render(request, 'home.html', context=data)

