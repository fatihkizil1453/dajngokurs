# apps/disputes/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Dispute, DisputeMessage
from .serializers import DisputeSerializer, DisputeMessageSerializer

class DisputeViewSet(viewsets.ModelViewSet):
    serializer_class = DisputeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Dispute.objects.all()
        # Users see disputes they created OR disputes against their sales (if seller)
        return Dispute.objects.filter(created_by=user) | Dispute.objects.filter(order__seller=user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def message(self, request, pk=None):
        dispute = self.get_object()
        content = request.data.get('content')
        
        if not content:
            return Response({'error': 'Content required'}, status=400)

        DisputeMessage.objects.create(
            dispute=dispute,
            sender=request.user,
            content=content
        )
        return Response({'status': 'Message sent'})
