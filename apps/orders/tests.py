# apps/orders/tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.products.models import Product, ProductVariant
from .models import Order, SellerOrder, OrderItem

User = get_user_model()

class OrderFlowTests(APITestCase):
    def setUp(self):
        # Users
        self.buyer = User.objects.create_user(email='buyer@test.com', password='password', role='BUYER')
        self.seller1 = User.objects.create_user(email='s1@test.com', password='password', role='SELLER')
        self.seller2 = User.objects.create_user(email='s2@test.com', password='password', role='SELLER')
        
        # Products
        p1 = Product.objects.create(seller=self.seller1, name='P1', slug='p1', status='ACTIVE')
        self.v1 = ProductVariant.objects.create(product=p1, sku='SKU1', name='V1', price=100.00, stock_quantity=10)
        
        p2 = Product.objects.create(seller=self.seller2, name='P2', slug='p2', status='ACTIVE')
        self.v2 = ProductVariant.objects.create(product=p2, sku='SKU2', name='V2', price=50.00, stock_quantity=5)

    def test_checkout_multi_vendor(self):
        self.client.force_authenticate(user=self.buyer)
        url = '/api/orders/buyer/checkout/'
        data = {
            'items': [
                {'variant_id': self.v1.id, 'quantity': 2}, # Seller 1: 200.00
                {'variant_id': self.v2.id, 'quantity': 1}  # Seller 2: 50.00
            ],
            'shipping_address': {'address': '123 St'},
            'billing_address': {'address': '123 St'}
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify Global Order
        order = Order.objects.first()
        self.assertEqual(order.total_amount, 250.00)
        self.assertEqual(order.status, 'PAID')
        
        # Verify Seller Splits
        self.assertEqual(SellerOrder.objects.count(), 2)
        s1_order = SellerOrder.objects.get(seller=self.seller1)
        self.assertEqual(s1_order.total_amount, 200.00)
        
        # Verify Stock Reduction
        self.v1.refresh_from_db()
        self.assertEqual(self.v1.stock_quantity, 8)

    def test_stock_concurrency_fail(self):
        # Try to buy more than available
        self.client.force_authenticate(user=self.buyer)
        url = '/api/orders/buyer/checkout/'
        data = {
            'items': [{'variant_id': self.v2.id, 'quantity': 100}], # Has 5
            'shipping_address': {}, 'billing_address': {}
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Insufficient stock', str(response.data))

    def test_seller_shipping_permission(self):
        # Create an order first
        order = Order.objects.create(buyer=self.buyer, total_amount=100, status='PAID', shipping_address={}, billing_address={})
        s_order = SellerOrder.objects.create(order=order, seller=self.seller1, total_amount=100, status='PROCESSING')
        
        # Seller 2 tries to ship Seller 1's order
        self.client.force_authenticate(user=self.seller2)
        url = f'/api/orders/seller/{s_order.id}/ship/'
        data = {'tracking_number': '123', 'carrier_name': 'UPS'}
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) # Can't see it

        # Seller 1 ships it
        self.client.force_authenticate(user=self.seller1)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        s_order.refresh_from_db()
        self.assertEqual(s_order.status, 'SHIPPED')
