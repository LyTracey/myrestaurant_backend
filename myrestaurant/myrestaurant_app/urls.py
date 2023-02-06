from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"orders",  views.OrderViewSet, basename="order")
router.register(r"menu", views.MenuViewSet, basename="menu")
router.register(r"inventory", views.InventoryViewSet, basename="inventory")
router.register(r"dashboard", views.DashboardViewSet, basename="dashboard")

urlpatterns = [
    path('', include(router.urls))
]

for url in router.urls:
    print(str(url) + "\n")