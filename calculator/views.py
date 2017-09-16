from django.shortcuts import render, HttpResponse

# Create your views here.

def calculator(request):
    return HttpResponse("calculator")