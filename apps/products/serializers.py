# apps/products/serializers.py
from rest_framework import serializers
from .models import Product, ProductVariant, BundleItem, ProductImage, Category
from apps.accounts.serializers import SellerProfileSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'image', 'order']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_main']

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        exclude = ['created_at', 'updated_at']
        read_only_fields = ['product']

class BundleItemSerializer(serializers.ModelSerializer):
    variant_sku = serializers.CharField(source='variant.sku', read_only=True)
    
    class Meta:
        model = BundleItem
        fields = ['variant', 'variant_sku', 'quantity']

class ProductListSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source='seller.seller_profile.business_name', read_only=True, default="MarketPlus")
    category = CategorySerializer(read_only=True)
    price_range = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    stock_quantity = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'seller_name', 'category', 'status', 'is_bundle', 'price_range', 'price', 'image', 'average_rating', 'review_count', 'stock_quantity']
        
    def get_price_range(self, obj):
        variants = obj.variants.all()
        if not variants:
            return "0.00"
        prices = [v.price for v in variants]
        if len(prices) == 1:
            return str(prices[0])
        return f"{min(prices)} - {max(prices)}"

    def get_price(self, obj):
        variants = obj.variants.all()
        if not variants:
            return 0.00
        return min([v.price for v in variants])

    def get_image(self, obj):
        img = obj.images.filter(is_main=True).first()
        if not img:
            img = obj.images.first()
        if img and img.image:
            return img.image.url
        return ""

    def get_stock_quantity(self, obj):
        """Calculate total stock across all variants"""
        variants = obj.variants.all()
        if not variants:
            return 0
        return sum([v.stock_quantity for v in variants])

class ProductDetailSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    bundle_items = BundleItemSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    seller_name = serializers.CharField(source='seller.seller_profile.business_name', read_only=True, default="MarketPlus")
    
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['seller', 'slug', 'status', 'created_at', 'updated_at', 'average_rating', 'review_count']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        img = instance.images.filter(is_main=True).first() or instance.images.first()
        rep['image'] = img.image.url if (img and img.image) else ""
        return rep

class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, required=False)
    
    class Meta:
        model = Product
        exclude = ['seller', 'status', 'slug']
        
    def create(self, validated_data):
        variants_data = validated_data.pop('variants', [])
        from django.utils.text import slugify
        
        name = validated_data.get('name', 'Product')
        base_slug = slugify(name)
        import uuid
        validated_data['slug'] = f"{base_slug}-{uuid.uuid4().hex[:6]}"
        
        product = Product.objects.create(**validated_data)
        
        for variant_data in variants_data:
            ProductVariant.objects.create(product=product, **variant_data)
            
        return product
