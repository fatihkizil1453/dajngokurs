# apps/orders/serializers.py
from rest_framework import serializers
from .models import Order, SellerOrder, OrderItem, Shipment
from apps.products.models import ProductVariant

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='variant.product.name', read_only=True)
    variant_name = serializers.SerializerMethodField()
    sku = serializers.CharField(source='variant.sku', read_only=True)
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'variant', 'product_name', 'variant_name', 'sku', 'quantity', 'unit_price', 'total_price', 'image']
        read_only_fields = ['unit_price', 'total_price']

    def get_variant_name(self, obj):
        # Get full variant name with product name
        product_name = obj.variant.product.name
        variant_name = obj.variant.name
        if variant_name and variant_name != 'Default':
            return f"{product_name} ({variant_name})"
        return product_name

    def get_image(self, obj):
        # Retrieve image from product
        img = obj.variant.product.images.filter(is_main=True).first()
        if not img:
            img = obj.variant.product.images.first()
        if img:
            return img.image.url
        return ""

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = ['tracking_number', 'carrier_name', 'shipped_at', 'estimated_delivery']

class SellerOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    shipment = ShipmentSerializer(read_only=True)
    seller_name = serializers.CharField(source='seller.seller_profile.business_name', read_only=True)
    buyer_name = serializers.SerializerMethodField()
    shipping_address = serializers.SerializerMethodField()
    
    class Meta:
        model = SellerOrder
        fields = ['id', 'seller_name', 'buyer_name', 'status', 'total_amount', 'items', 'shipment', 'shipping_address', 'created_at']
    
    def get_buyer_name(self, obj):
        buyer = obj.order.buyer
        return f"{buyer.first_name} {buyer.last_name}".strip() or buyer.email
    
    def get_shipping_address(self, obj):
        return obj.order.shipping_address

class OrderDetailSerializer(serializers.ModelSerializer):
    seller_orders = SellerOrderSerializer(many=True, read_only=True)
    items = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'total_amount', 'currency', 'status', 'shipping_address', 'billing_address', 'seller_orders', 'items', 'created_at']

    def get_items(self, obj):
        # Flatten items from all seller packets
        all_items = []
        for packet in obj.seller_orders.all():
            for item in packet.items.all():
                data = OrderItemSerializer(item).data
                # Add seller info to item for display
                data['seller'] = packet.seller.seller_profile.business_name
                all_items.append(data)
        return all_items

class CartItemInputSerializer(serializers.Serializer):
    variant_id = serializers.IntegerField(required=False, allow_null=True)
    product_id = serializers.IntegerField(required=False, allow_null=True)
    quantity = serializers.IntegerField(min_value=1)

class CheckoutSerializer(serializers.Serializer):
    items = CartItemInputSerializer(many=True)
    shipping_address = serializers.JSONField()
    billing_address = serializers.JSONField()

class ShipmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = ['tracking_number', 'carrier_name', 'estimated_delivery']
