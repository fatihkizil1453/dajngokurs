# apps/products/tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Product

User = get_user_model()

class ProductTests(APITestCase):
    def setUp(self):
        self.seller = User.objects.create_user(email='seller@test.com', password='password', role='SELLER')
        self.other_seller = User.objects.create_user(email='other@test.com', password='password', role='SELLER')
        self.buyer = User.objects.create_user(email='buyer@test.com', password='password', role='BUYER')
        
    def test_create_product_as_seller(self):
        self.client.force_authenticate(user=self.seller)
        url = '/api/products/'
        data = {
            'name': 'Test Product',
            'description': 'A detailed description',
            'variants': [
                {'sku': 'SKU1', 'name': 'Red', 'price': '10.00', 'stock_quantity': 5}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.first().seller, self.seller)

    def test_create_product_as_buyer_forbidden(self):
        self.client.force_authenticate(user=self.buyer)
        url = '/api/products/'
        data = {'name': 'Fail'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_seller_update_own_product(self):
        product = Product.objects.create(seller=self.seller, name='Original', status='ACTIVE', slug='orig')
        self.client.force_authenticate(user=self.seller)
        url = f'/api/products/{product.slug}/'
        response = self.client.patch(url, {'name': 'Updated'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.name, 'Updated')

    def test_seller_cannot_update_others_product(self):
        product = Product.objects.create(seller=self.other_seller, name='Other', status='ACTIVE', slug='other')
        self.client.force_authenticate(user=self.seller)
        url = f'/api/products/{product.slug}/'
        response = self.client.patch(url, {'name': 'Hacked'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) # Or 403 depending on QuerySet filtering
