# disputes/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User
from apps.orders.models import SellerOrder

class Dispute(models.Model):
    class Status(models.TextChoices):
        OPEN = 'OPEN', _('Açık')
        UNDER_REVIEW = 'UNDER_REVIEW', _('İnceleme Altında')
        RESOLVED_REFUND = 'RESOLVED_REFUND', _('Çözüldü (İade Yapıldı)')
        RESOLVED_NO_REFUND = 'RESOLVED_NO_REFUND', _('Çözüldü (İade Yapılmadı)')
        CANCELLED = 'CANCELLED', _('İptal Edildi')

    class Reason(models.TextChoices):
        NOT_RECEIVED = 'NOT_RECEIVED', _('Ürün teslim alınmadı')
        DAMAGED = 'DAMAGED', _('Ürün hasarlı')
        NOT_AS_DESCRIBED = 'NOT_AS_DESCRIBED', _('Tanımlandığı gibi değil')
        OTHER = 'OTHER', _('Diğer')

    order = models.ForeignKey(SellerOrder, on_delete=models.CASCADE, related_name='disputes', verbose_name=_('sipariş'))
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_disputes', verbose_name=_('oluşturan'))
    
    reason = models.CharField(_('neden'), max_length=50, choices=Reason.choices)
    description = models.TextField(_('açıklama'))
    
    status = models.CharField(_('durum'), max_length=30, choices=Status.choices, default=Status.OPEN)
    
    # Admin Resolution Tracking
    resolved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='resolved_disputes',
        limit_choices_to={'role': 'ADMIN'}, # Best effort filter
        verbose_name=_('çözen yönetici')
    )
    resolved_at = models.DateTimeField(_('çözülme tarihi'), null=True, blank=True)
    admin_decision_note = models.TextField(_('yönetici karar notu'), blank=True)
    
    created_at = models.DateTimeField(_('oluşturulma tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('güncellenme tarihi'), auto_now=True)

    class Meta:
        verbose_name = _('İtiraz')
        verbose_name_plural = _('İtirazlar')

    def __str__(self):
        return f"Dispute #{self.id} on Order #{self.order.id}"

class DisputeMessage(models.Model):
    dispute = models.ForeignKey(Dispute, on_delete=models.CASCADE, related_name='messages', verbose_name=_('itiraz'))
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('gönderici'))
    content = models.TextField(_('içerik'))
    attachment = models.FileField(_('ek'), upload_to='dispute_attachments/', blank=True, null=True)
    
    created_at = models.DateTimeField(_('oluşturulma tarihi'), auto_now_add=True)

    class Meta:
        verbose_name = _('İtiraz Mesajı')
        verbose_name_plural = _('İtiraz Mesajları')

    def __str__(self):
        return f"Msg on Dispute #{self.dispute.id}"
