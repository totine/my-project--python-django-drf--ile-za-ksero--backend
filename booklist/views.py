from django.shortcuts import render, HttpResponse

from booklist.models import Category
from calculator.models import Bind, XeroBaseBookCalc


def home(request):
    standard_xero_cost = 0.07
    search = request.GET.get('search', '')
    books = XeroBaseBookCalc.objects.all() if not search else XeroBaseBookCalc.objects.filter(book__title__icontains=search)
    bind = Bind.objects.all()[0]
    categories = Category.objects.all()
    cost_per_page = int(request.GET.get('cost_per_page', '')) / 100 if request.GET.get('cost_per_page', '') else standard_xero_cost

    for book in books:
        book.set_actual_bind(bind)
        book.set_actual_price(cost_per_page)

    data = {"books": books, "categories": categories, "bind": bind, "cost_per_page": cost_per_page, "search": search}
    return render(request, 'home.html', context=data)

