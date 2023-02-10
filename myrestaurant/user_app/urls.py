from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework import routers
from .views import MyUserViewset

router = routers.DefaultRouter()
router.register("users", MyUserViewset, basename="user")

urlpatterns = [
    path('', include('rest_framework.urls', namespace='rest_framework')),
    path('token/', views.obtain_auth_token),
] + router.urls