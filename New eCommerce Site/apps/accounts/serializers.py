# apps/accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import SellerProfile, BuyerProfile

User = get_user_model()

class SellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        fields = ['business_name', 'tax_id', 'commission_rate', 'status']
        read_only_fields = ['commission_rate', 'status']

class BuyerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerProfile
        fields = ['loyalty_points', 'preferences']
        read_only_fields = ['loyalty_points']

class UserSerializer(serializers.ModelSerializer):
    seller_profile = SellerProfileSerializer(read_only=True)
    buyer_profile = BuyerProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'is_verified', 'seller_profile', 'buyer_profile']
        read_only_fields = ['role', 'is_verified']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.Role.choices)
    business_name = serializers.CharField(required=False, write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'role', 'business_name']

    def create(self, validated_data):
        role = validated_data.pop('role')
        business_name = validated_data.pop('business_name', '')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(
            email=validated_data['email'],
            password=password,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=role
        )
        
        if role == User.Role.SELLER:
            SellerProfile.objects.create(user=user, business_name=business_name or f"Store {user.id}")
        elif role == User.Role.BUYER:
            BuyerProfile.objects.create(user=user)
            
        return user
