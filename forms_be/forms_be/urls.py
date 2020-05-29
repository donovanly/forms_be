from core.views import FormViewSet
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from user_management.views import UserViewSet


router = routers.DefaultRouter()
router.register(r'forms', FormViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
