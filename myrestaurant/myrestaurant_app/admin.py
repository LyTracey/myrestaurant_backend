from django.contrib import admin
from rest_framework import routers
from .views import OrderViewSet, MenuViewSet, InventoryViewSet

router = routers.SimpleRouter()
router.register(r'orders', OrderViewSet)
router.register(r'menu', MenuViewSet)
router.register(r'inventory', InventoryViewSet)

urlpatterns = router.urls