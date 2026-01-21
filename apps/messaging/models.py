# messaging/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User
from apps.orders.models import SellerOrder

class Conversation(models.Model):
    # Conversations are strictly linked to an Order (Context)
    order = models.ForeignKey(SellerOrder, on_delete=models.CASCADE, related_name='conversations', verbose_name=_('sipariş'))
    
    participants = models.ManyToManyField(User, related_name='conversations', verbose_name=_('katılımcılar'))
    
    created_at = models.DateTimeField(_('oluşturulma tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('güncellenme tarihi'), auto_now=True) # Last message time

    class Meta:
        verbose_name = _('Sohbet')
        verbose_name_plural = _('Sohbetler')

    def __str__(self):
        return f"Chat for Order #{self.order.id}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages', verbose_name=_('sohbet'))
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name=_('gönderici'))
    
    content = models.TextField(_('içerik'))
    is_system_message = models.BooleanField(_('sistem mesajı mı'), default=False)
    
    read_by = models.ManyToManyField(User, related_name='read_messages', blank=True, verbose_name=_('okuyanlar'))
    
    created_at = models.DateTimeField(_('gönderilme tarihi'), auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = _('Mesaj')
        verbose_name_plural = _('Mesajlar')

    def __str__(self):
        return f"Msg {self.id} from {self.sender}"
