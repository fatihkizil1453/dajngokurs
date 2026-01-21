# products/admin.py
from django.contrib import admin
from .models import Product, ProductVariant, BundleItem, ProductImage, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order',)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    classes = ['collapse']
    verbose_name = "Ürün Görseli"
    verbose_name_plural = "Ürün Görselleri"

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    show_change_link = True
    fields = ('sku', 'price', 'stock_quantity', 'name')
    verbose_name = "Varyasyon / Fiyat & Stok"
    verbose_name_plural = "Varyasyonlar (Fiyat & Stok)"

class BundleItemInline(admin.TabularInline):
    model = BundleItem
    extra = 1
    fk_name = 'bundle_product'
    autocomplete_fields = ['variant']
    classes = ['collapse']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'category', 'status', 'is_bundle', 'created_at')
    list_filter = ('category', 'status', 'created_at', 'seller')
    search_fields = ('name', 'slug', 'seller__email', 'variants__sku')
    prepopulated_fields = {'slug': ('name',)}
    
    inlines = [ProductImageInline, ProductVariantInline, BundleItemInline]
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('name', 'slug', 'category', 'description', 'status', 'seller')
        }),
        ('Gelişmiş Ayarlar', {
            'classes': ('collapse',),
            'fields': ('is_18_plus', 'requires_prescription', 'is_preorder', 'preorder_release_date', 'is_bundle', 'average_rating', 'review_count')
        }),
    )

    def save_model(self, request, obj, form, change):
        # If no seller is provided (Admin), leave it null (Platform Product)
        pass
        super().save_model(request, obj, form, change)

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'sku', 'price', 'stock_quantity')
    search_fields = ('product__name', 'sku', 'name')
    list_filter = ('product__seller',)
    autocomplete_fields = ['product']
