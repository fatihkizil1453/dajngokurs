# apps/reviews/views.py
from rest_framework import viewsets, permissions, filters
from .models import Review
from .serializers import ReviewSerializer
from apps.accounts.permissions import IsBuyer

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['product__id']

    def get_queryset(self):
        queryset = Review.objects.filter(status=Review.Status.PUBLISHED)
        
        if self.request.user.is_authenticated:
            # User sees all published + their own pending/rejected
            queryset = queryset | Review.objects.filter(author=self.request.user)
            queryset = queryset.distinct()

        product_id = self.request.query_params.get('product')
        if product_id:
            queryset = queryset.filter(product_id=product_id)
            
        return queryset

    def perform_create(self, serializer):
        # Ideally verify 'order_item' here based on logic
        serializer.save(author=self.request.user)
