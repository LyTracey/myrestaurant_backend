from django.urls import path, include
from rest_framework import routers
from .views import TokenView, ProfileViewset, RegisterViewset
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

router = routers.DefaultRouter()

urlpatterns = [
    # path('', include('rest_framework.urls', namespace='rest_framework')),
    path("profile/<str:username>/", ProfileViewset.as_view(), name="profile"),
    path("register/", RegisterViewset.as_view(), name="user"),
    path('login/', TokenView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
] + router.urls