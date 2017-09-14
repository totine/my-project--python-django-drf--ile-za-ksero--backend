from django.shortcuts import render, HttpResponse

from booklist.models import XeroBook, Category, Bind


def home(request):
    standard_xero_cost = 0.07
    books = XeroBook.objects.all()
    bind = Bind.objects.all()[0]
    categories = Category.objects.all()

    cost_per_page = int(request.GET.get('cost_per_page', '')) / 100

    for book in books:
        book.set_actual_bind(bind)
        book.set_actual_price(cost_per_page if cost_per_page else standard_xero_cost)

    data = {"books": books, "categories": categories, "bind": bind}
    return render(request, 'home.html', context=data)

