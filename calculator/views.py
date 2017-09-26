from decimal import Decimal

from django.shortcuts import render, HttpResponse


# Create your views here.
from calculator.models import XeroCalc, XeroSimpleCalc, XeroBookCalc, XeroList


def calculator(request):
    request.session.flush()
    standard_xero_cost = 0.07
    default_bind_cost = 0
    xero_cost = XeroSimpleCalc()
    xero_cost.cost_per_page = standard_xero_cost
    xero_cost.number_of_pages_from_form = 0
    xero_cost.bind_cost = default_bind_cost
    try:
        xero_list = XeroList.objects.get(pk=request.session["xero_list_id"])
    except:
        xero_list = XeroList()
    xero_list.save()
    request.session["xero_list_id"] = xero_list.id
    data = {"xero_cost": xero_cost, "xero_list": xero_list}
    return render(request, 'calc.html', context=data)


def calculate(request):
    cost_per_page = Decimal(request.POST.get('cost_per_page', 0))/100
    number_of_pages = int(request.POST['number_of_pages'])
    bind_cost = Decimal(request.POST.get('bind_cost', 0))
    xero_cost = XeroSimpleCalc()
    xero_cost.cost_per_page = cost_per_page
    xero_cost.number_of_pages_from_form = number_of_pages
    xero_cost.bind_cost = bind_cost
    xero_cost.name = ""
    xero_cost.save()
    xero_list = XeroList.objects.get(pk=request.session["xero_list_id"]) if "xero_list_id" in request.session else XeroList()
    request.session["xero_list_id"] = xero_list.id
    data = {"xero_cost": xero_cost, "xero_list": xero_list}
    request.session['xero_cost_id'] = xero_cost.id
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
    xero_cost.save()
    xero_list = XeroList.objects.get(pk=request.session["xero_list_id"]) if "xero_list_id" in request.session else XeroList()
    request.session['xero_cost_id'] = xero_cost.id
    data = {"xero_cost": xero_cost, "xero_list": xero_list}
    return render(request, 'calc.html', context=data)


def add_xero_to_list(request):

    xero_cost = XeroCalc.get_xero_calc_by_id(request.session["xero_cost_id"])
    xero_list = XeroList.objects.get(pk=request.session["xero_list_id"])
    xero_list.add(xero_cost)
    xero_cost.save()
    xero_list.save()
    data = {"xero_cost": xero_cost, "xero_list": xero_list}
    return render(request, 'calc.html', context=data)


