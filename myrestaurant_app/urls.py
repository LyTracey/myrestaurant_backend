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
    path('dashboard-stock/', views.DashboardStockView.as_view(), name="dashboard_stock"),
    path("archive/orders/",  views.ArchivedOrdersView.as_view(), name="archived_orders"),
    path("inventory-reference/", views.InventoryReferenceView.as_view(), name="inventory_reference"),
    path("reset-db/", views.reset_db, name="reset_db")
]

for url in router.urls:
    print(str(url) + "\n")