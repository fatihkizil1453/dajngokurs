# apps/products/views.py
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, ProductVariant, Category
from .serializers import ProductListSerializer, ProductDetailSerializer, ProductCreateUpdateSerializer, ProductVariantSerializer, CategorySerializer
from apps.accounts.permissions import IsSeller, IsOwnerOrReadOnly

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().order_by('order', 'name')
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

class ProductViewSet(viewsets.ModelViewSet):
    # lookup_field = 'slug' # Default to pk (id) for now to match frontend
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductDetailSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsSeller(), IsOwnerOrReadOnly()] # Or IsAdmin
        return [permissions.AllowAny()]

    def get_queryset(self):
        qs = Product.objects.filter(status=Product.Status.ACTIVE)
        
        # Admin or Seller viewing their own products
        if self.request.user.is_authenticated:
            if self.request.query_params.get('mine') and self.request.user.role == 'SELLER':
                return Product.objects.filter(seller=self.request.user)
        
        # Filter by Category
        category_slug = self.request.query_params.get('category')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
            
        return qs.order_by('-created_at')

    def perform_create(self, serializer):
        if self.request.user.role == 'SELLER':
            serializer.save(seller=self.request.user, status=Product.Status.ACTIVE)
        else:
            serializer.save()
    
    @action(detail=True, methods=['post'])
    def upload_image(self, request, pk=None):
        """Upload product image"""
        from .models import ProductImage
        product = self.get_object()
        
        # Check if user owns this product
        if product.seller != request.user:
            return Response({'error': 'You do not own this product'}, status=403)
        
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({'error': 'No image provided'}, status=400)
        
        is_main = request.data.get('is_main', 'false').lower() == 'true'
        
        # If this is set as main, unset other main images
        if is_main:
            ProductImage.objects.filter(product=product, is_main=True).update(is_main=False)
        
        # Create the image
        product_image = ProductImage.objects.create(
            product=product,
            image=image_file,
            is_main=is_main
        )
        
        return Response({
            'id': product_image.id,
            'image': product_image.image.url,
            'is_main': product_image.is_main
        })

class VariantViewSet(viewsets.ModelViewSet):
    # Only for sellers editing variants
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [permissions.IsAuthenticated, IsSeller]
    
    def get_queryset(self):
        return ProductVariant.objects.filter(product__seller=self.request.user)
