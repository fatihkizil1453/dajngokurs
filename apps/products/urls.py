# apps/products/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, VariantViewSet, CategoryViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('variants', VariantViewSet, basename='variants')
router.register('', ProductViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
]
