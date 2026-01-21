# apps/reviews/serializers.py
from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        if obj.author.first_name:
            return f"{obj.author.first_name} {obj.author.last_name[:1]}." if obj.author.last_name else obj.author.first_name
        return obj.author.email.split('@')[0][:3] + "***"
    
    class Meta:
        model = Review
        fields = ['id', 'product', 'author', 'rating', 'title', 'comment', 'status', 'created_at']
        read_only_fields = ['status', 'author']
