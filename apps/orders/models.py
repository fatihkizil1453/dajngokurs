# orders/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User
from apps.products.models import ProductVariant

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Ödeme Bekliyor')
        PAID = 'PAID', _('Ödendi')
        PARTIALLY_FULFILLED = 'PARTIALLY_FULFILLED', _('Kısmen Tamamlandı')
        COMPLETED = 'COMPLETED', _('Tamamlandı')
        CANCELLED = 'CANCELLED', _('İptal Edildi')

    buyer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders', verbose_name=_('alıcı'))
    
    total_amount = models.DecimalField(_('toplam tutar'), max_digits=12, decimal_places=2)
    currency = models.CharField(_('para birimi'), max_length=3, default='TL')
    
    status = models.CharField(_('durum'), max_length=20, choices=Status.choices, default=Status.PENDING)
    payment_method = models.CharField(_('ödeme yöntemi'), max_length=50)
    transaction_id = models.CharField(_('işlem numarası (ID)'), max_length=100, blank=True)
    
    shipping_address = models.JSONField(_('teslimat adresi'), default=dict, help_text=_("Sipariş anındaki teslimat adresi kopyası"))
    billing_address = models.JSONField(_('fatura adresi'), default=dict, help_text=_("Sipariş anındaki fatura adresi kopyası"))
    
    created_at = models.DateTimeField(_('oluşturulma tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('güncellenme tarihi'), auto_now=True)

    class Meta:
        verbose_name = _('Sipariş')
        verbose_name_plural = _('Siparişler')

    def __str__(self):
        return f"Order #{self.id} - {self.buyer}"

class SellerOrder(models.Model):
    """
    Splits the main Order into sub-orders for each seller (Multi-Vendor support).
    Also known as an 'Order Packet`.
    """
    class Status(models.TextChoices):
        WAITING_CONFIRMATION = 'WAITING', _('Satıcı Onayı Bekliyor')
        PROCESSING = 'PROCESSING', _('Hazırlanıyor')
        SHIPPED = 'SHIPPED', _('Kargoya Verildi')
        DELIVERED = 'DELIVERED', _('Teslim Edildi')
        CANCELLED = 'CANCELLED', _('İptal Edildi')
        RETURNED = 'RETURNED', _('İade Edildi')

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='seller_orders', verbose_name=_('ana sipariş'))
    seller = models.ForeignKey(User, on_delete=models.PROTECT, related_name='seller_orders', verbose_name=_('satıcı'))
    
    total_amount = models.DecimalField(_('toplam tutar'), max_digits=12, decimal_places=2)
    commission_amount = models.DecimalField(_('komisyon tutarı'), max_digits=12, decimal_places=2, default=0)
    
    status = models.CharField(_('durum'), max_length=20, choices=Status.choices, default=Status.WAITING_CONFIRMATION)
    
    created_at = models.DateTimeField(_('oluşturulma tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('güncellenme tarihi'), auto_now=True)

    class Meta:
        verbose_name = _('Satıcı Siparişi')
        verbose_name_plural = _('Satıcı Siparişleri')

    def __str__(self):
        return f"SubOrder #{self.id} from Order #{self.order.id}"

class OrderItem(models.Model):
    seller_order = models.ForeignKey(SellerOrder, on_delete=models.CASCADE, related_name='items', verbose_name=_('satıcı siparişi'))
    variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT, verbose_name=_('varyasyon'))
    
    quantity = models.PositiveIntegerField(_('miktar'))
    unit_price = models.DecimalField(_('birim fiyat'), max_digits=12, decimal_places=2) # Price at time of purchase
    total_price = models.DecimalField(_('toplam fiyat'), max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = _('Sipariş Kalemi')
        verbose_name_plural = _('Sipariş Kalemleri')

    def __str__(self):
        return f"{self.quantity}x {self.variant.sku}"

class Shipment(models.Model):
    seller_order = models.OneToOneField(SellerOrder, on_delete=models.CASCADE, related_name='shipment', verbose_name=_('satıcı siparişi'))
    tracking_number = models.CharField(_('takip numarası'), max_length=100)
    carrier_name = models.CharField(_('kargo firması'), max_length=100)
    shipped_at = models.DateTimeField(_('kargoya verilme tarihi'), auto_now_add=True)
    estimated_delivery = models.DateField(_('tahmini teslim tarihi'), null=True, blank=True)

    class Meta:
        verbose_name = _('Sevkiyat')
        verbose_name_plural = _('Sevkiyatlar')

    def __str__(self):
        return f"{self.carrier_name}: {self.tracking_number}"
