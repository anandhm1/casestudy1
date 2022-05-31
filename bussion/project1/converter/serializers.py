from rest_framework import serializers
from .models import Company,MoneyConverter

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"

class MoneyConverterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoneyConverter
        fields = "__all__"