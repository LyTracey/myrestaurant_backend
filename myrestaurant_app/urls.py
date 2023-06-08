from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"orders",  views.OrderViewSet, basename="order")
router.register(r"menu", views.MenuViewSet, basename="menu")
router.register(r"inventory", views.InventoryViewSet, basename="inventory")

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', views.DashboardView.as_view(), name="dashboard"),
    path("archive/orders/",  views.ArchivedOrdersView.as_view(), name="archived-orders")
]

for url in router.urls:
    print(str(url) + "\n")