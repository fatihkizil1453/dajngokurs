# apps/orders/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BuyerOrderViewSet, SellerOrderViewSet

router = DefaultRouter()
router.register('buyer', BuyerOrderViewSet, basename='buyer-orders')
router.register('seller', SellerOrderViewSet, basename='seller-orders')

urlpatterns = [
    path('', include(router.urls)),
]
