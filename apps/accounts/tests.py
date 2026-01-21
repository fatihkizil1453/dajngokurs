# apps/accounts/tests.py
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import SellerProfile, BuyerProfile

User = get_user_model()

class AuthTests(APITestCase):
    def test_register_seller(self):
        url = '/api/auth/register/'
        data = {
            'email': 'seller@example.com',
            'password': 'strongpassword123',
            'role': 'SELLER',
            'business_name': 'My Awesome Store'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='seller@example.com').exists())
        self.assertTrue(SellerProfile.objects.filter(business_name='My Awesome Store').exists())

    def test_register_buyer(self):
        url = '/api/auth/register/'
        data = {
            'email': 'buyer@example.com',
            'password': 'strongpassword123',
            'role': 'BUYER'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(BuyerProfile.objects.filter(user__email='buyer@example.com').exists())

    def test_login(self):
        user = User.objects.create_user(email='test@example.com', password='password', role='BUYER')
        url = '/api/auth/login/'
        data = {'email': 'test@example.com', 'password': 'password'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('email', response.data)
