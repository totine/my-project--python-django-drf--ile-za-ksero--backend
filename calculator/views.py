from decimal import Decimal

import math
from django.shortcuts import render, HttpResponse, redirect


# Create your views here.
from calculator.models import XeroCalc, XeroSimpleCalc, XeroBookCalc, XeroList, Bind, XeroByWeightCalc


def calculator(request):
    try:
        bind = Bind.objects.get(name="main")
    except:
        bind = Bind()

    xero_cost = XeroSimpleCalc() if not request.session["xero_cost_id"] or not XeroCalc.get_xero_calc_by_id(request.session["xero_cost_id"]) \
        else XeroCalc.get_xero_calc_by_id(request.session["xero_cost_id"])
    try:
        xero_list = XeroList.objects.get(pk=request.session["xero_list_id"])
    except:
        xero_list = XeroList()
    xero_list.save()
    suggested_bind_price = bind.get_bind_price(xero_cost.number_of_cards)
    request.session["xero_list_id"] = xero_list.id
    data = {"xero_cost": xero_cost, "xero_list": xero_list, "suggested_bind_price": suggested_bind_price}
    return render(request, 'calc.html', context=data)


def calculate(request):
    sides_dict = {"onesided": False, "twosided": False, "mixonesided": False, "mixtwosided": False}
    cost_name = request.POST["name"]
    cost_per_page = Decimal(request.POST.get('cost_per_page', 0))/100
    number_of_pages_or_cards = int(request.POST['number_of_pages_or_cards'])
    sides_dict[request.POST.get('sides', '')] = True
    number_of_one_sided_pages_in_two_sided_mix = int(request.POST['onesided-in-mixtwosided']) if request.POST['onesided-in-mixtwosided'] else 0
    number_of_two_sided_pages_in_one_sided_mix = int(request.POST['twosided-in-mixonesided']) if request.POST['twosided-in-mixonesided'] else 0
    bind_cost = Decimal(request.POST.get('bind_cost', 0))
    xero_cost = XeroSimpleCalc()
    xero_cost.cost_per_page = cost_per_page
    xero_cost.is_cards_in_form = True if request.POST['pages_or_cards'] == 'cards' else False
    xero_cost.number_of_cards_from_form = number_of_pages_or_cards if xero_cost.is_cards_in_form else int(math.ceil(number_of_pages_or_cards/2))
    xero_cost.bind_cost = bind_cost
    xero_cost.bind_ranges = Bind.objects.get(name="main")
    xero_cost.name = cost_name
    xero_cost.is_one_sided = sides_dict["onesided"]
    xero_cost.is_two_sided = sides_dict["twosided"]
    xero_cost.is_mix_with_one_sided_advantage = sides_dict["mixonesided"]
    xero_cost.is_mix_with_two_sided_advantage = sides_dict["mixtwosided"]
    xero_cost.one_sided_pages_in_mix = number_of_one_sided_pages_in_two_sided_mix if number_of_one_sided_pages_in_two_sided_mix and xero_cost.is_mix_with_two_sided_advantage else 0
    xero_cost.two_sided_pages_in_mix = number_of_two_sided_pages_in_one_sided_mix if number_of_two_sided_pages_in_one_sided_mix and xero_cost.is_mix_with_one_sided_advantage else 0
    xero_cost.save()
    xero_list = XeroList.objects.get(pk=request.session["xero_list_id"]) if "xero_list_id" in request.session else XeroList()
    request.session["xero_list_id"] = xero_list.id
    request.session['xero_cost_id'] = xero_cost.id
    return redirect("/")


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
    request.session['xero_cost_id'] = xero_cost.id
    return redirect("/")


def add_xero_to_list(request):
    xero_cost = XeroCalc.get_xero_calc_by_id(request.session["xero_cost_id"])
    xero_list = XeroList.objects.get(pk=request.session["xero_list_id"])
    xero_list.add(xero_cost)
    xero_cost.save()
    xero_list.save()
    return redirect("/")


def delete_cost(request, costid):
    xero_cost = XeroCalc.get_xero_calc_by_id(costid)
    xero_cost.xero_cost_list = None
    xero_cost.save()
    return redirect("/")


def reset_xero_list(request):
    del request.session['xero_list_id']
    return redirect("/")


def calculate_by_weight(request):
    sides_dict = {"onesided": False, "twosided": False, "mixonesided": False, "mixtwosided": False}
    cost_name = request.POST["name"]
    cost_per_page = Decimal(request.POST.get('cost_per_page', 0))/100
    sides_dict[request.POST.get('sides', '')] = True
    number_of_one_sided_pages_in_two_sided_mix = int(request.POST['onesided-in-mixtwosided']) if request.POST['onesided-in-mixtwosided'] else 0
    number_of_two_sided_pages_in_one_sided_mix = int(request.POST['twosided-in-mixonesided']) if request.POST['twosided-in-mixonesided'] else 0
    bind_cost = Decimal(request.POST.get('bind_cost', 0))
    xero_cost = XeroByWeightCalc() if not 'costid' in request.POST else XeroCalc.get_xero_calc_by_id(int(request.POST['costid']))
    xero_cost.cost_per_page = cost_per_page
    xero_cost.is_bind = True if 'is-bind' in request.POST else False
    xero_cost.weight = int(request.POST['weight'])
    xero_cost.bind_cost = bind_cost
    xero_cost.bind_ranges = Bind.objects.get(name="main")
    xero_cost.name = cost_name
    xero_cost.is_one_sided = sides_dict["onesided"]
    xero_cost.is_two_sided = sides_dict["twosided"]
    xero_cost.is_mix_with_one_sided_advantage = sides_dict["mixonesided"]
    xero_cost.is_mix_with_two_sided_advantage = sides_dict["mixtwosided"]
    xero_cost.one_sided_pages_in_mix = number_of_one_sided_pages_in_two_sided_mix if number_of_one_sided_pages_in_two_sided_mix and xero_cost.is_mix_with_two_sided_advantage else 0
    xero_cost.two_sided_pages_in_mix = number_of_two_sided_pages_in_one_sided_mix if number_of_two_sided_pages_in_one_sided_mix and xero_cost.is_mix_with_one_sided_advantage else 0
    xero_cost.save()
    xero_list = XeroList.objects.get(pk=request.session["xero_list_id"]) if "xero_list_id" in request.session else XeroList()
    request.session["xero_list_id"] = xero_list.id
    request.session['xero_cost_id'] = xero_cost.id
    return redirect("/")


def xerolist_view(request, xerolistid):
    xerolist = XeroList.objects.get(pk=xerolistid)
    data = {'xero_list': xerolist}
    return render(request, 'xerolist.html', context=data)


def xerolist_delete(request, xerolistid):
    xerolist = XeroList.objects.get(pk=xerolistid)
    xerolist.delete()
    xerolist.save()
    return redirect('/')


def cost_edit(request, costid):
    xero_cost = XeroCalc.get_xero_calc_by_id(costid)
    xero_type = xero_cost.cost_short_name
    data = {'xero_cost': xero_cost, 'xero_type': xero_type}
    return render(request, 'cost-edit.html', context=data)


def cost_view(request, costid):
    xero_cost = XeroCalc.get_xero_calc_by_id(costid)
    data = {'xero_cost': xero_cost}
    return render(request, 'cost-view.html', context=data)