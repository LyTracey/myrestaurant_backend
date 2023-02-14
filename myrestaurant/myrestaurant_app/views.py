from .models import Inventory, Order, Menu, Dashboard, MenuInventory
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import OrderSerializer, MenuSerializer, InventorySerializer, DashboardSerializer
from rest_framework.parsers import MultiPartParser, FormParser
import logging
from .utils import overwrite
from .permissions import ReadOnly, Staff
from rest_framework.authentication import TokenAuthentication


logger = logging.getLogger(__name__)


class OrderViewSet(viewsets.ModelViewSet): 
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [Staff|ReadOnly]


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
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [Staff|ReadOnly]


class DashboardViewSet(viewsets.ModelViewSet):
    # Calls functions from utils.py to calculate statistics
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer
    permission_classes = [Staff|ReadOnly]