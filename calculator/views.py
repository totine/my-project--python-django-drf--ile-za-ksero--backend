from decimal import Decimal

from django.shortcuts import render, HttpResponse

# Create your views here.
from calculator.models import XeroCalc, XeroSimpleCalc, XeroBookCalc


def calculator(request):
    standard_xero_cost = 0.07
    default_bind_cost = 0
    xero_cost = XeroSimpleCalc()
    xero_cost.cost_per_page = standard_xero_cost
    xero_cost.number_of_pages_from_form = 0
    xero_cost.bind_cost = default_bind_cost
    data = {"xero_cost": xero_cost}

    return render(request, 'calc.html', context=data)


def calculate(request):
    print(request.POST)
    cost_per_page = Decimal(request.POST.get('cost_per_page', 0))/100
    number_of_pages = int(request.POST['number_of_pages'])
    bind_cost = Decimal(request.POST.get('bind_cost', 0))
    xero_cost = XeroSimpleCalc()
    xero_cost.cost_per_page = cost_per_page
    xero_cost.number_of_pages_from_form = number_of_pages
    xero_cost.bind_cost = bind_cost
    data = {"xero_cost": xero_cost}
    return render(request, 'calc.html', context=data)


def calculate_book(request):
    arabic_pages = int(request.POST.get('book_pages_arabic', 0))
    roman_pages = int(request.POST.get('book_pages_roman', 0))
    bind_cost = Decimal(request.POST.get('bind_cost', 0))
    cost_per_page = Decimal(request.POST.get('cost_per_page', 0)) / 100
    xero_cost = XeroBookCalc()
    xero_cost.book_pages_arabic = arabic_pages
    xero_cost.book_pages_roman = roman_pages
    xero_cost.bind_cost = bind_cost
    xero_cost.cost_per_page = cost_per_page
    data = {"xero_cost": xero_cost}
    return render(request, 'calc.html', context=data)