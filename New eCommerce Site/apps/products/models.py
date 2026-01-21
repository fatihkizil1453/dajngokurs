# products/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User

class Category(models.Model):
    name = models.CharField(_('kategori adı'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    icon = models.CharField(_('ikon (emoji)'), max_length=50, help_text="Emoji", blank=True)
    image = models.ImageField(_('ikon görseli'), upload_to='categories/', null=True, blank=True)
    order = models.PositiveIntegerField(_('sıralama'), default=0)
    
    class Meta:
        verbose_name = _('Kategori')
        verbose_name_plural = _('Kategoriler')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class Product(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', _('Taslak')
        PENDING = 'PENDING', _('İnceleme Bekliyor')
        ACTIVE = 'ACTIVE', _('Aktif')
        SUSPENDED = 'SUSPENDED', _('Askıya Alındı')
        ARCHIVED = 'ARCHIVED', _('Arşivlendi')

    seller = models.ForeignKey(User, on_delete=models.PROTECT, related_name='products', limit_choices_to={'role': 'SELLER'}, verbose_name=_('satıcı'), null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name=_('kategori'))
    
    name = models.CharField(_('ürün adı'), max_length=255)
    slug = models.SlugField(_('kısa isim (slug)'), unique=True, max_length=255)
    description = models.TextField(_('açıklama'))
    
    status = models.CharField(_('durum'), max_length=20, choices=Status.choices, default=Status.DRAFT)
    
    # Restrictions
    is_18_plus = models.BooleanField(_('18+ yaş sınırı'), default=False)
    requires_prescription = models.BooleanField(_('reçete gerektirir'), default=False)
    is_preorder = models.BooleanField(_('ön sipariş'), default=False)
    preorder_release_date = models.DateTimeField(_('ön sipariş çıkış tarihi'), null=True, blank=True)
    
    is_bundle = models.BooleanField(_('paket ürün mü'), default=False, help_text=_("Eğer doğruysa, bu ürün diğer varyasyonlardan oluşur"))
    
    # Rating/Score
    average_rating = models.DecimalField(_('ortalama puan'), max_digits=3, decimal_places=2, default=0.00)
    review_count = models.PositiveIntegerField(_('değerlendirme sayısı'), default=0)

    created_at = models.DateTimeField(_('oluşturulma tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('güncellenme tarihi'), auto_now=True)

    class Meta:
        verbose_name = _('Ürün')
        verbose_name_plural = _('Ürünler')

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name=_('ürün'))
    image = models.ImageField(_('görsel'), upload_to='products/')
    is_main = models.BooleanField(_('ana görsel mi'), default=False)
    
    class Meta:
        verbose_name = _('Ürün Görseli')
        verbose_name_plural = _('Ürün Görselleri')

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants', verbose_name=_('ürün'))
    sku = models.CharField(_('stok kodu (SKU)'), max_length=100, unique=True)
    name = models.CharField(_('varyasyon adı'), max_length=255, help_text=_("ör. Standart, Beden L, Kırmızı"), default='Standart')
    
    price = models.DecimalField(_('fiyat'), max_digits=12, decimal_places=2)
    compare_at_price = models.DecimalField(_('indirim öncesi fiyat'), max_digits=12, decimal_places=2, null=True, blank=True)
    stock_quantity = models.IntegerField(_('stok adedi'), default=0)
    
    weight_g = models.IntegerField(_('ağırlık (gram)'), default=0, help_text=_("Kargo için gram cinsinden ağırlık"))
    
    attributes = models.JSONField(_('özellikler'), default=dict, blank=True, help_text=_("Dinamik özellikler ör. {'renk': 'kırmızı'}"))

    created_at = models.DateTimeField(_('oluşturulma tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('güncellenme tarihi'), auto_now=True)

    class Meta:
        verbose_name = _('Ürün Varyasyonu')
        verbose_name_plural = _('Ürün Varyasyonları')

    def __str__(self):
        return f"{self.product.name} - {self.name} ({self.sku})"

class BundleItem(models.Model):
    """
    Defines the contents of a bundle product.
    A 'Bundle' is a Product (is_bundle=True) that contains other ProductVariants.
    """
    bundle_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bundle_items', verbose_name=_('paket ürün'))
    variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT, related_name='in_bundles', verbose_name=_('varyasyon'))
    quantity = models.PositiveIntegerField(_('miktar'), default=1)

    class Meta:
        unique_together = ('bundle_product', 'variant')
        verbose_name = _('Paket İçeriği')
        verbose_name_plural = _('Paket İçerikleri')

    def __str__(self):
        return f"{self.quantity}x {self.variant.sku} in {self.bundle_product.name}"
