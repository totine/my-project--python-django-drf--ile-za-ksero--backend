from rest_framework import serializers

from calculator.models import XeroSimpleCalc, XeroCalc, XeroBookCalc, XeroByWeightCalc


class XeroCalcSerializer(serializers.ModelSerializer):
    class Meta:
        model = XeroCalc
        fields = '__all__'


class XeroSimpleCalcSerializer(serializers.ModelSerializer):
    class Meta:
        model = XeroSimpleCalc
        fields = '__all__'


class XeroBookCalcSerializer(serializers.ModelSerializer):
    class Meta:
        model = XeroBookCalc
        fields = '__all__'


class XeroByWeightCalcSerializer(serializers.ModelSerializer):
    class Meta:
        model = XeroByWeightCalc
        fields = '__all__'

