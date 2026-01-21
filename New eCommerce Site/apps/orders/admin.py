# orders/admin.py
from django.contrib import admin
from .models import Order, SellerOrder, OrderItem, Shipment

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('variant', 'quantity', 'unit_price', 'total_price')
    can_delete = False

class SellerOrderInline(admin.StackedInline):
    model = SellerOrder
    extra = 0
    readonly_fields = ('seller', 'total_amount', 'commission_amount', 'status')
    show_change_link = True
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'total_amount', 'currency', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'currency')
    search_fields = ('id', 'buyer__email', 'transaction_id')
    readonly_fields = ('created_at', 'updated_at', 'total_amount', 'shipping_address', 'billing_address', 'payment_method')
    inlines = [SellerOrderInline]

class ShipmentInline(admin.StackedInline):
    model = Shipment
    extra = 0

@admin.register(SellerOrder)
class SellerOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_link', 'seller', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'order__id', 'seller__email')
    readonly_fields = ('total_amount', 'commission_amount')
    inlines = [OrderItemInline, ShipmentInline]
    
    def order_link(self, obj):
        return f"Order #{obj.order.id}"
    order_link.short_description = "Parent Order"

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('tracking_number', 'carrier_name', 'seller_order', 'shipped_at')
    search_fields = ('tracking_number', 'seller_order__id')
