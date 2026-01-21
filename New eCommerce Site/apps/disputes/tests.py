# apps/disputes/tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.orders.models import Order, SellerOrder
from .models import Dispute

User = get_user_model()

class DisputeTests(APITestCase):
    def setUp(self):
        self.buyer = User.objects.create_user(email='buyer@test.com', role='BUYER')
        self.seller = User.objects.create_user(email='seller@test.com', role='SELLER')
        
        order = Order.objects.create(buyer=self.buyer, total_amount=100, status='PAID', shipping_address={}, billing_address={})
        self.s_order = SellerOrder.objects.create(order=order, seller=self.seller, total_amount=100, status='SHIPPED')

    def test_create_dispute(self):
        self.client.force_authenticate(user=self.buyer)
        url = '/api/disputes/'
        data = {
            'order': self.s_order.id,
            'reason': 'NOT_RECEIVED',
            'description': 'Where is it?'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Dispute.objects.count(), 1)
        self.assertEqual(Dispute.objects.first().status, 'OPEN')

    def test_seller_sees_dispute(self):
        Dispute.objects.create(order=self.s_order, created_by=self.buyer, reason='DAMAGED', description='Broken')
        
        self.client.force_authenticate(user=self.seller)
        url = '/api/disputes/'
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
