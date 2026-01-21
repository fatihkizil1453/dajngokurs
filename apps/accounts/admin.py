# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, SellerProfile, BuyerProfile

class SellerProfileInline(admin.StackedInline):
    model = SellerProfile
    can_delete = False
    verbose_name_plural = 'Seller Profile'
    extra = 0

class BuyerProfileInline(admin.StackedInline):
    model = BuyerProfile
    can_delete = False
    verbose_name_plural = 'Buyer Profile'
    extra = 0

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Status', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'risk_score')}),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'is_verified', 'risk_score', 'is_active')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'is_verified')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    inlines = [SellerProfileInline, BuyerProfileInline]
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        inlines = []
        if obj.role == User.Role.SELLER or hasattr(obj, 'seller_profile'):
            inlines.append(SellerProfileInline)
        if obj.role == User.Role.BUYER or hasattr(obj, 'buyer_profile'):
            inlines.append(BuyerProfileInline)
        return [inline(self.model, self.admin_site) for inline in inlines]

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'status', 'commission_rate', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('business_name', 'user__email', 'tax_id')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status',)

@admin.register(BuyerProfile)
class BuyerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'loyalty_points', 'created_at')
    search_fields = ('user__email',)
    readonly_fields = ('created_at', 'updated_at')
