# campaigns/admin.py
from django.contrib import admin
from .models import Campaign, Coupon, CouponUsage

class CouponInline(admin.TabularInline):
    model = Coupon
    extra = 1
    fields = ('code', 'discount_type', 'discount_value', 'usage_limit', 'end_date')

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active', 'is_currently_active')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('name',)
    inlines = [CouponInline]

class CouponUsageInline(admin.TabularInline):
    model = CouponUsage
    extra = 0
    readonly_fields = ('user', 'order', 'used_at')
    can_delete = False
    max_num = 0

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'campaign', 'discount_type', 'discount_value', 'usage_limit', 'created_at')
    search_fields = ('code', 'campaign__name')
    list_filter = ('discount_type', 'created_at')
    inlines = [CouponUsageInline]
