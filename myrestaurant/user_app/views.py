from django.shortcuts import render
from .serializers import CustomerSerializer
from .models import Customer
from rest_framework import viewsets


class CustomerViewSet(viewsets.ModelViewSet): 
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
