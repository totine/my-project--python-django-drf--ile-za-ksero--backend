from decimal import Decimal

from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.utils.crypto import get_random_string
from calculator.models import XeroCalc, XeroSimpleCalc, XeroBookCalc, XeroList, Bind, XeroByWeightCalc, XeroPriceList
from calculator.serializers import XeroSimpleCalcSerializer, XeroCalcSerializer, XeroBookCalcSerializer, XeroByWeightCalcSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class CostListView(APIView):
    def get(self, request):
        costs = XeroCalc.objects.all()
        serializer = XeroSimpleCalcSerializer(costs, many=True)
        return Response(serializer.data)


class CostDetails(APIView):
    def get(self, request, costid):
        cost = XeroCalc.get_xero_calc_by_id(costid)
        serializers = {"simple": XeroSimpleCalcSerializer,
                       "book": XeroBookCalcSerializer,
                       "weight": XeroByWeightCalcSerializer}
        serializer = serializers[cost.cost_short_name](cost)
        return Response(serializer.data)




