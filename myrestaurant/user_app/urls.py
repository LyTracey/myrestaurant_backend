from django.urls import path, include
from rest_framework.authtoken import views

urlpatterns = [
    path('', include('rest_framework.urls', namespace='rest_framework')),
    path('token/', views.obtain_auth_token),
]