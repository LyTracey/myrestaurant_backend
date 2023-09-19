from django.urls import path
from rest_framework import routers
from .views import ProfileViewset, RegisterViewset, MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

router = routers.DefaultRouter()

urlpatterns = [
    path("profile/<str:username>/", ProfileViewset.as_view(), name="profile"),
    path("register/", RegisterViewset.as_view(), name="user"),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
] + router.urls

