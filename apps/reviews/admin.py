# reviews/admin.py
from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'author', 'rating', 'status', 'created_at')
    list_filter = ('status', 'rating', 'created_at')
    search_fields = ('product__name', 'author__email', 'title', 'comment')
    readonly_fields = ('created_at', 'updated_at', 'author', 'product', 'order_item')
    list_editable = ('status',)
    
    actions = ['mark_published', 'mark_rejected']

    @admin.action(description='Mark selected reviews as Published')
    def mark_published(self, request, queryset):
        queryset.update(status=Review.Status.PUBLISHED)

    @admin.action(description='Mark selected reviews as Rejected')
    def mark_rejected(self, request, queryset):
        queryset.update(status=Review.Status.REJECTED)
