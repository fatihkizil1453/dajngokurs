# campaigns/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User

class Campaign(models.Model):
    name = models.CharField(_('kampanya adı'), max_length=255)
    description = models.TextField(_('açıklama'), blank=True)
    
    start_date = models.DateTimeField(_('başlangıç tarihi'))
    end_date = models.DateTimeField(_('bitiş tarihi'))
    
    is_active = models.BooleanField(_('aktif mi'), default=True)
    
    created_at = models.DateTimeField(_('oluşturulma tarihi'), auto_now_add=True)

    class Meta:
        verbose_name = _('Kampanya')
        verbose_name_plural = _('Kampanyalar')

    def is_currently_active(self):
        from django.utils import timezone
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date

    def __str__(self):
        return self.name

class Coupon(models.Model):
    class DiscountType(models.TextChoices):
        PERCENTAGE = 'PERCENTAGE', _('Yüzde')
        FIXED_AMOUNT = 'FIXED', _('Sabit Tutar')

    code = models.CharField(_('kupon kodu'), max_length=50, unique=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='coupons', null=True, blank=True, verbose_name=_('kampanya'))
    
    discount_type = models.CharField(_('indirim türü'), max_length=20, choices=DiscountType.choices)
    discount_value = models.DecimalField(_('indirim değeri'), max_digits=10, decimal_places=2)
    
    min_spend_amount = models.DecimalField(_('minimum harcama tutarı'), max_digits=10, decimal_places=2, default=0)
    
    usage_limit = models.PositiveIntegerField(_('kullanım sınırı'), null=True, blank=True, help_text=_("Bu kuponun toplam kaç kez kullanılabileceği"))
    usage_limit_per_user = models.PositiveIntegerField(_('kullanıcı başı sınır'), default=1)
    
    from django.utils import timezone
    start_date = models.DateTimeField(_('başlangıç tarihi'), default=timezone.now)
    end_date = models.DateTimeField(_('bitiş tarihi'), null=True, blank=True)
    
    created_at = models.DateTimeField(_('oluşturulma tarihi'), auto_now_add=True)

    class Meta:
        verbose_name = _('Kupon')
        verbose_name_plural = _('Kuponlar')

    def __str__(self):
        return self.code

class CouponUsage(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='usages', verbose_name=_('kupon'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coupon_usages', verbose_name=_('kullanıcı'))
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('sipariş')) 
    used_at = models.DateTimeField(_('kullanılma tarihi'), auto_now_add=True)

    class Meta:
        verbose_name = _('Kupon Kullanımı')
        verbose_name_plural = _('Kupon Kullanımları')
    
    def __str__(self):
        return f"{self.user} used {self.coupon}"
