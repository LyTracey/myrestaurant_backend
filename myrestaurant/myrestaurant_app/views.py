from .models import Inventory, Order, Menu, MenuInventory
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import OrderSerializer, MenuSerializer, InventorySerializer, DashboardSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .permissions import ReadOnly, Staff
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from myrestaurant_app.scripts.dashboard_utils import summary_statistics
from myrestaurant_app.scripts.myrestaurant_utils import ordered_lte_available
from rest_framework import status
import logging
from operator import itemgetter
import json
# from .scripts.utils import overwrite
# from rest_framework.authentication import TokenAuthentication


logger = logging.getLogger(__name__)


class OrderViewSet(viewsets.ModelViewSet): 
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [Staff|ReadOnly]

    def create(self, request, *args, **kwargs):
        quantity = json.loads(request.data.get("quantity"))
        if ordered_lte_available(quantity, Menu):
            return super().create(request, *args, **kwargs)
        return Response({"error": "Quantity ordered is greater than available"}, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, *args, **kwargs):
        quantity = json.loads(request.data.get("quantity"))
        if ordered_lte_available(quantity, Menu):
            return super().partial_update(request, *args, **kwargs)
        return Response({"error": "Quantity ordered is greater than available"}, status=status.HTTP_400_BAD_REQUEST)
    

class MenuViewSet(viewsets.ModelViewSet): 
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    lookup_field = "slug"
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [Staff|ReadOnly]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = MenuSerializer(instance, request.data, partial=True)
        if serializer.is_valid():
            # overwrite(serializer)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            # overwrite(serializer)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [Staff|ReadOnly]


class DashboardView(RetrieveUpdateAPIView, GenericAPIView):
    serializer_class = DashboardSerializer
    permission_classes = [Staff|ReadOnly]

    def retrieve(self, request, *args, **kwargs):
        data = summary_statistics()
        return Response(data=data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        serializer = DashboardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        start_date, end_date, frequency = itemgetter('start_date', 'end_date', 'frequency')(serializer.data)

        data = summary_statistics(start_date, end_date, frequency)
        return Response(data=data, status=status.HTTP_200_OK)

