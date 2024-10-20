from .models import Inventory, Order, Menu
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import OrderSerializer, MenuSerializer, InventorySerializer, DashboardSerializer, InventoryReferenceSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .permissions import ReadOnly, Staff, Chef, Sales, Manager, Superuser
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, ListAPIView
from myrestaurant_app.scripts.dashboard_utils import summary_statistics
from myrestaurant_app.scripts.view_utils import ordered_lte_available
from rest_framework import status
import logging
from operator import itemgetter
import json
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from myrestaurant_app.scripts.serializer_utils import return_ingredients
from rest_framework.decorators import api_view, permission_classes
from scripts.database_setup import run
import os


logger = logging.getLogger(__name__)

# Override authentication method to prevent authentication for public pages
class JWTAuthenticationSafe(JWTAuthentication):
    def authenticate(self, request):
        try:
            return super().authenticate(request=request)
        except InvalidToken:
            return None

class OrderViewSet(viewsets.ModelViewSet): 
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [Staff & (Manager | Sales)]

    def create(self, request, *args, **kwargs):
        quantity = json.loads(request.data.get("quantity"))
        if ordered_lte_available(quantity, Menu):
            return super().create(request, *args, **kwargs)
        return Response({"error": "Quantity ordered is greater than available"}, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, *args, **kwargs):

        # Check checkboxes are ticked in order prepared > delivered > complete
        order = Order.objects.get(pk=kwargs['pk'])
        if request.data.get("delivered", False) and not order.prepared:
            return Response({"error": "Please make sure order is prepared first."})
        elif request.data.get("complete", False) and (not order.prepared or not order.delivered):
            return Response({"error": "Please make sure order is prepared and delivered first."})

        # Check if quantity ordered is greater than available
        if request.data.get("quantity", False):
            quantity = json.loads(request.data.get("quantity"))
            if not ordered_lte_available(quantity, Menu):
                return Response({"error": "Quantity ordered is greater than available"}, status=status.HTTP_400_BAD_REQUEST)
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """
            Add ingredients back to inventory if order is cancelled.
        """
        
        pk = kwargs["pk"]
        order = Order.objects.get(pk=pk)
        return_ingredients(order)
    
        return super().destroy(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        queryset = Order.objects.filter(complete=False)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ArchivedOrdersView(generics.ListAPIView):
    queryset = Order.objects.filter(complete=True)
    serializer_class = OrderSerializer
    permission_classes = [Staff &  (Manager | Sales)]
        

class MenuViewSet(viewsets.ModelViewSet): 
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    lookup_field = "id"
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [(Staff & (Manager | Chef)) | ReadOnly]
    authentication_classes = [JWTAuthenticationSafe]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = MenuSerializer(instance, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def create(self, request, *args, **kwargs):
        serializer = MenuSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    # permission_classes = [(Staff & (Manager | Chef))]
    permission_classes = []
    lookup_field = "id"
    authentication_classes = []


class InventoryReferenceView (ListAPIView, GenericAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventoryReferenceSerializer
    permission_classes = [ReadOnly]
    authentication_classes = [JWTAuthenticationSafe]


class DashboardView(RetrieveUpdateAPIView, GenericAPIView):
    serializer_class = DashboardSerializer
    permission_classes = [Staff & (Manager | Sales)]

    def retrieve(self, request, *args, **kwargs):
        data = summary_statistics()
        return Response(data=data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        serializer = DashboardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        start_date, end_date, frequency = itemgetter('start_date', 'end_date', 'frequency')(serializer.data)

        data = summary_statistics(start_date, end_date, frequency)
        return Response(data=data, status=status.HTTP_200_OK)
    
class DashboardStockView(ListAPIView, GenericAPIView):
    permission_classes = [ReadOnly]

    def list(self, request, *args, **kwargs):
        statistics = summary_statistics()
        stock_data = {
            "low_stock": statistics["low_stock"],
            "out_of_stock": statistics["out_of_stock"]
        }
        return Response(data=stock_data, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([Superuser])
def reset_db(request):
    """
        Reset database data.
    """
    if request.method == "POST":
        try:
            db_key = request.data.get("reset_db_key", default="")
            if db_key == os.getenv("RESET_DB_SECRET"):
                run()
                return Response("Database successfully reset.", status=status.HTTP_200_OK)
        except:
            return Response("Reset key is invalid.", status=status.HTTP_401_UNAUTHORIZED)
    
    return Response("Unknown method.", status=status.HTTP_405_METHOD_NOT_ALLOWED)