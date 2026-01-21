# apps/messaging/serializers.py
from rest_framework import serializers
from .models import Conversation, Message
from apps.accounts.serializers import UserSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender_id = serializers.IntegerField(source='sender.id', read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'sender_id', 'content', 'created_at', 'is_system_message']

class ConversationSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    order = serializers.IntegerField(source='order.id', read_only=True)
    participants = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['id', 'order', 'participants', 'updated_at', 'last_message']
    
    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        if last_msg:
             return MessageSerializer(last_msg).data
        return None
