# accounts/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Yönetici')
        SELLER = 'SELLER', _('Satıcı')
        BUYER = 'BUYER', _('Alıcı')

    username = None
    email = models.EmailField(_('e-posta adresi'), unique=True)
    role = models.CharField(_('rol'), max_length=10, choices=Role.choices, default=Role.BUYER)
    
    # Common status flags
    is_verified = models.BooleanField(_('doğrulandı mı'), default=False)
    risk_score = models.FloatField(_('risk skoru'), default=0.0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _('Kullanıcı')
        verbose_name_plural = _('Kullanıcılar')

    def __str__(self):
        return self.email

class SellerProfile(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Onay Bekliyor')
        APPROVED = 'APPROVED', _('Onaylandı')
        SUSPENDED = 'SUSPENDED', _('Askıya Alındı')
        REJECTED = 'REJECTED', _('Reddedildi')

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile', verbose_name=_('kullanıcı'))
    business_name = models.CharField(_('mağaza adı'), max_length=255)
    tax_id = models.CharField(_('vergi numarası'), max_length=50, blank=True)
    status = models.CharField(_('durum'), max_length=20, choices=Status.choices, default=Status.PENDING)
    commission_rate = models.DecimalField(_('komisyon oranı'), max_digits=5, decimal_places=2, default=10.00)  # Percentage
    
    created_at = models.DateTimeField(_('oluşturulma tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('güncellenme tarihi'), auto_now=True)

    class Meta:
        verbose_name = _('Satıcı Profili')
        verbose_name_plural = _('Satıcı Profilleri')

    def __str__(self):
        return self.business_name

class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_profile', verbose_name=_('kullanıcı'))
    loyalty_points = models.IntegerField(_('sadakat puanı'), default=0)
    preferences = models.JSONField(_('tercihler'), default=dict, blank=True)
    
    created_at = models.DateTimeField(_('oluşturulma tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('güncellenme tarihi'), auto_now=True)

    class Meta:
        verbose_name = _('Alıcı Profili')
        verbose_name_plural = _('Alıcı Profilleri')

    def __str__(self):
        return f"Buyer: {self.user.email}"
