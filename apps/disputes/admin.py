# disputes/admin.py
from django.contrib import admin
from .models import Dispute, DisputeMessage

class DisputeMessageInline(admin.TabularInline):
    model = DisputeMessage
    extra = 0
    readonly_fields = ('sender', 'content', 'attachment', 'created_at')
    can_delete = False
    
    def has_add_permission(self, request, obj):
        return False

@admin.register(Dispute)
class DisputeAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'created_by', 'reason', 'status', 'created_at')
    list_filter = ('status', 'reason', 'created_at')
    search_fields = ('order__id', 'description', 'created_by__email')
    readonly_fields = ('order', 'created_by', 'created_at', 'updated_at', 'resolved_by', 'resolved_at')
    inlines = [DisputeMessageInline]
    
    fieldsets = (
        ('Dispute Details', {
            'fields': ('order', 'created_by', 'reason', 'description', 'status')
        }),
        ('Admin Resolution', {
            'fields': ('admin_decision_note', 'resolved_by', 'resolved_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data:
            from django.utils import timezone
            # If status changed to a resolved state, auto-set resolver
            if obj.status in [
                Dispute.Status.RESOLVED_REFUND, 
                Dispute.Status.RESOLVED_NO_REFUND, 
                Dispute.Status.CANCELLED
            ]:
                if not obj.resolved_by:
                    obj.resolved_by = request.user
                if not obj.resolved_at:
                    obj.resolved_at = timezone.now()
        super().save_model(request, obj, form, change)
