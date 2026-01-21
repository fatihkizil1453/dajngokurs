# messaging/admin.py
from django.contrib import admin
from .models import Conversation, Message

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('sender', 'content', 'created_at', 'is_system_message', 'read_by')
    can_delete = False
    
    def has_add_permission(self, request, obj):
        return False

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'created_at', 'updated_at')
    search_fields = ('order__id',)
    readonly_fields = ('order', 'participants')
    inlines = [MessageInline]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'sender', 'created_at', 'is_system_message')
    list_filter = ('is_system_message', 'created_at')
    search_fields = ('content', 'sender__email', 'conversation__order__id')
    readonly_fields = ('conversation', 'sender', 'content', 'read_by', 'created_at')
    
    def has_add_permission(self, request):
        return False
