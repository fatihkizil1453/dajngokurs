# apps/messaging/views.py
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users see conversations they are part of
        return Conversation.objects.filter(participants=self.request.user).order_by('-updated_at')

    @action(detail=True, methods=['get', 'post'])
    def messages(self, request, pk=None):
        conversation = self.get_object()
        
        if request.method == 'GET':
            msgs = conversation.messages.all()
            return Response(MessageSerializer(msgs, many=True).data)
        
        if request.method == 'POST':
            content = request.data.get('content')
            if not content:
                return Response({'error': 'Content required'}, status=400)
                
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            # Update conversion timestamp
            conversation.save()
            return Response({'status': 'Message sent'})
