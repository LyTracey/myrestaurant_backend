from django.shortcuts import render
from .serializers import LoginSerializer
from rest_framework import views
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from django.contrib.auth.views import LoginView, LogoutView