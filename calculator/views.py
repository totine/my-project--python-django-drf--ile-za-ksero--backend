from django.shortcuts import render, HttpResponse

# Create your views here.


def calculator(request):
    standard_xero_cost = 0.07
    number_of_pages = request.GET.get('number', '') if request.GET.get('number', '') else 0
    cost_per_page = int(request.GET.get('cost_per_page', '')) / 100 if request.GET.get('cost_per_page', '') else standard_xero_cost
    total_cost = round(int(number_of_pages) * cost_per_page, 2)

    data = {"cost_per_page": cost_per_page, "number_of_pages": number_of_pages, "total_cost": total_cost}

    return render(request, 'calc.html', context=data)


def calculate(request):

    return HttpResponse("calculate")
