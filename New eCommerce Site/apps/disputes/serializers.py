# apps/disputes/serializers.py
from rest_framework import serializers
from .models import Dispute, DisputeMessage

class DisputeMessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = DisputeMessage
        fields = '__all__'
        read_only_fields = ['dispute', 'sender']

class DisputeSerializer(serializers.ModelSerializer):
    messages = DisputeMessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Dispute
        fields = '__all__'
        read_only_fields = ['created_by', 'status', 'resolved_by', 'resolved_at', 'admin_decision_note']
