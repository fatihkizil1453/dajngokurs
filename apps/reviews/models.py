# reviews/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User
from apps.products.models import Product

class Review(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Moderasyon Bekliyor')
        PUBLISHED = 'PUBLISHED', _('Yayınlandı')
        REJECTED = 'REJECTED', _('Reddedildi')

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name=_('ürün'))
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('yazar'))
    
    order_item = models.ForeignKey(
        'orders.OrderItem', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='reviews',
        verbose_name=_('sipariş kalemi')
    )
    
    from django.core.validators import MinValueValidator, MaxValueValidator
    rating = models.PositiveSmallIntegerField(_('puan'), validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(_('başlık'), max_length=100, blank=True)
    comment = models.TextField(_('yorum'))
    
    status = models.CharField(_('durum'), max_length=20, choices=Status.choices, default=Status.PUBLISHED)
    moderation_note = models.TextField(_('moderasyon notu'), blank=True, help_text=_("Reddedilme nedeni veya dahili notlar"))
    
    created_at = models.DateTimeField(_('oluşturulma tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('güncellenme tarihi'), auto_now=True)

    class Meta:
        unique_together = ('product', 'author') # One review per product per user
        verbose_name = _('Değerlendirme')
        verbose_name_plural = _('Değerlendirmeler')

    def __str__(self):
        return f"{self.rating}* - {self.product.name}"
