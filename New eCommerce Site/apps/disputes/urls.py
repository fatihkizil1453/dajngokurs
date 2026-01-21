# apps/disputes/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DisputeViewSet

router = DefaultRouter()
router.register('', DisputeViewSet, basename='disputes')

urlpatterns = [
    path('', include(router.urls)),
]
