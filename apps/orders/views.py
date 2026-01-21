# apps/orders/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from .models import Order, SellerOrder, OrderItem, Shipment
from apps.products.models import ProductVariant
from .serializers import OrderDetailSerializer, SellerOrderSerializer, CheckoutSerializer, ShipmentUpdateSerializer
from apps.accounts.permissions import IsBuyer, IsSeller
from apps.messaging.models import Conversation, Message

class BuyerOrderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Buyer viewing their own Global Orders
    """
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsBuyer]

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user).order_by('-created_at')

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        
        # Check eligibility
        # Check global status
        if order.status in [Order.Status.COMPLETED, Order.Status.CANCELLED]:
            return Response({'error': 'Bu sipariş iptal edilemez.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if any sub-order is shipped
        if order.seller_orders.filter(status__in=[SellerOrder.Status.SHIPPED, SellerOrder.Status.DELIVERED]).exists():
             return Response({'error': 'Siparişin bir kısmı kargolandığı için tamamı iptal edilemez.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Cancel order
        order.status = Order.Status.CANCELLED
        order.save()
        
        # Cancel sub-orders
        # Cancel sub-orders
        for so in order.seller_orders.all():
             # Only if not shipped
             if so.status not in [SellerOrder.Status.SHIPPED, SellerOrder.Status.DELIVERED]:
                 so.status = SellerOrder.Status.CANCELLED
                 so.save()
                 
                 # Restore Stock
                 for item in so.items.all():
                     variant = item.variant
                     variant.stock_quantity += item.quantity
                     variant.save()
        
        return Response({'status': 'Order cancelled'})
    @action(detail=False, methods=['post'])
    @transaction.atomic
    def checkout(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        
        # 1. Validate Stock & Calculate Totals
        # 1. Validate Stock & Calculate Totals
        # Group by Seller
        seller_packets = {} # { seller_id: [ { variant, qty, price } ] }
        global_total = 0
        
        for item in data['items']:
            variant = None
            if item.get('variant_id'):
                variant = ProductVariant.objects.select_for_update().get(id=item['variant_id'])
            elif item.get('product_id'):
                variant = ProductVariant.objects.select_for_update().filter(product_id=item['product_id']).first()
                
            if not variant:
                return Response({'error': f"Product/Variant not found or unavailable"}, status=status.HTTP_400_BAD_REQUEST)

            qty = item['quantity']
            
            # Use safe stock check
            if variant.stock_quantity < qty:
                return Response({'error': f"Insufficient stock for {variant.name}"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Reduce Stock
            variant.stock_quantity -= qty
            variant.save()
            
            # Organize
            seller_id = variant.product.seller_id
            if seller_id not in seller_packets:
                seller_packets[seller_id] = []
            
            line_total = variant.price * qty
            global_total += line_total
            
            seller_packets[seller_id].append({
                'variant': variant,
                'quantity': qty,
                'unit_price': variant.price,
                'total_price': line_total
            })

        # 2. Create Global Order
        order = Order.objects.create(
            buyer=request.user,
            total_amount=global_total,
            shipping_address=data['shipping_address'],
            billing_address=data['billing_address'],
            status=Order.Status.PAID # Assuming payment mocked
        )

        # 3. Create Seller Orders (Packets)
        for seller_id, items in seller_packets.items():
            packet_total = sum(i['total_price'] for i in items)
            seller_order = SellerOrder.objects.create(
                order=order,
                seller_id=seller_id,
                total_amount=packet_total,
                status=SellerOrder.Status.WAITING_CONFIRMATION # Wait for seller to confirm
            )
            
            for i in items:
                OrderItem.objects.create(
                    seller_order=seller_order,
                    variant=i['variant'],
                    quantity=i['quantity'],
                    unit_price=i['unit_price'],
                    total_price=i['total_price']
                )

        return Response(OrderDetailSerializer(order).data, status=status.HTTP_201_CREATED)


class SellerOrderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Seller managing their received Sub-Orders
    """
    serializer_class = SellerOrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsSeller]

    def get_queryset(self):
        return SellerOrder.objects.filter(seller=self.request.user).order_by('-created_at')

    @action(detail=True, methods=['post'])
    def ship(self, request, pk=None):
        seller_order = self.get_object()
        
        if seller_order.status not in [SellerOrder.Status.PROCESSING, SellerOrder.Status.WAITING_CONFIRMATION]:
             return Response({'error': 'Order not ready for shipping'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ShipmentUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        Shipment.objects.create(seller_order=seller_order, **serializer.validated_data)
        
        seller_order.status = SellerOrder.Status.SHIPPED
        seller_order.save()
        
        return Response({'status': 'Order Shipped'})
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """
        Seller confirms the order and starts processing it.
        This also sends a system message to the buyer.
        """
        seller_order = self.get_object()
        
        if seller_order.status != SellerOrder.Status.WAITING_CONFIRMATION:
            return Response({'error': 'Order already processed'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update status to PROCESSING
        seller_order.status = SellerOrder.Status.PROCESSING
        seller_order.save()
        
        # Get or create conversation for this order
        conversation, created = Conversation.objects.get_or_create(
            order=seller_order
        )
        
        # Add participants if newly created
        if created:
            conversation.participants.add(seller_order.seller, seller_order.order.buyer)
        
        # Send system message to buyer
        Message.objects.create(
            conversation=conversation,
            sender=request.user,  # Seller
            content="Siparişiniz onaylandı ve hazırlanıyor.",
            is_system_message=True
        )
        
        # Update conversation timestamp
        conversation.save()
        
        return Response({'status': 'Order confirmed and buyer notified'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """
        Seller rejects the order.
        """
        seller_order = self.get_object()
        
        if seller_order.status != SellerOrder.Status.WAITING_CONFIRMATION:
            return Response({'error': 'Order already processed'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update status to CANCELLED
        seller_order.status = SellerOrder.Status.CANCELLED
        seller_order.save()
        
        # Restore Stock
        for item in seller_order.items.all():
             variant = item.variant
             variant.stock_quantity += item.quantity
             variant.save()

        # Get or create conversation for this order
        conversation, created = Conversation.objects.get_or_create(
            order=seller_order
        )
        
        # Add participants if newly created
        if created:
            conversation.participants.add(seller_order.seller, seller_order.order.buyer)
        
        # Send system message to buyer
        Message.objects.create(
            conversation=conversation,
            sender=request.user,  # Seller
            content="Siparişiniz reddedildi.",
            is_system_message=True
        )
        
        # Update conversation timestamp
        conversation.save()
        
        return Response({'status': 'Order rejected and buyer notified'})

