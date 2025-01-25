from decimal import Decimal
from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, EmailValidator, MaxValueValidator
from django.conf import settings
from django.db.models import Q
from typing import TYPE_CHECKING, Any
import uuid


if TYPE_CHECKING:
    from django.db.models.manager import Manager

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email: str, password: str | None, **extra_fields: Any):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str | None = None, **extra_fields: Any):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str | None = None, **extra_fields: Any):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, **extra_fields)
class User(AbstractUser):
    """
    Modelo de usuário customizado usando email como identificador principal
    """
    username = None  # Remove username field
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone number'), max_length=50, blank=True)
    locale = models.CharField(_('locale'), max_length=10, default='fr-FR')
    timezone = models.CharField(_('timezone'), max_length=50, default='Europe/Paris')
    profile_image = models.JSONField(_('profile image'), default=dict)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    security_settings = models.JSONField(default=dict)
    notification_settings = models.JSONField(default=dict)
    password = models.CharField(_('password'), max_length=128)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects: 'Manager[User]' = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

class BaseModel(models.Model):
    """
    Modelo base com campos comuns para todos os outros modelos
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(class)s_created',
        verbose_name=_('created by')
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(class)s_updated',
        verbose_name=_('updated by')
    )
    is_active = models.BooleanField(_('active'), default=True)
    metadata = models.JSONField(_('metadata'), default=dict)

    class Meta:
        abstract = True

class SystemConfiguration(BaseModel):
    """
    Configurações globais do sistema
    """
    key = models.CharField(_('key'), max_length=100, unique=True)
    value = models.JSONField(_('value'))
    description = models.TextField(_('description'), blank=True)
    is_public = models.BooleanField(_('public'), default=False)
    category = models.CharField(_('category'), max_length=100)
    
    class Meta:
        verbose_name = _('system configuration')
        verbose_name_plural = _('system configurations')
        ordering = ['category', 'key']

class Language(BaseModel):
    """
    Idiomas suportados pelo sistema
    """
    code = models.CharField(_('code'), max_length=10, unique=True, db_index=True)
    name = models.CharField(_('name'), max_length=100)
    native_name = models.CharField(_('native name'), max_length=100)
    flag_emoji = models.CharField(_('flag emoji'), max_length=10, blank=True)
    is_default = models.BooleanField(_('default'), default=False)
    date_format = models.CharField(_('date format'), max_length=50)
    number_format = models.JSONField(_('number format'), default=dict)
    currency_format = models.JSONField(_('currency format'), default=dict)
    
    class Meta:
        verbose_name = _('language')
        verbose_name_plural = _('languages')
        ordering = ['name']

    def save(self, *args, **kwargs):
        if self.is_default:
            Language.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)
class Currency(BaseModel):
    """
    Moedas suportadas pelo sistema
    """
    code = models.CharField(_('code'), max_length=3, unique=True, db_index=True)
    name = models.CharField(_('name'), max_length=100)
    symbol = models.CharField(_('symbol'), max_length=10)
    decimal_places = models.IntegerField(_('decimal places'), default=2, validators=[MinValueValidator(0), MaxValueValidator(10)])
    exchange_rate = models.DecimalField(
        _('exchange rate'),
        max_digits=20,
        decimal_places=10,
        default=Decimal('1.0'),
        validators=[MinValueValidator(0)]
    )
    is_default = models.BooleanField(_('default'), default=False)
    
    class Meta:
        verbose_name = _('currency')
        verbose_name_plural = _('currencies')
        ordering = ['code']

class Country(BaseModel):
    """
    Países suportados pelo sistema
    """
    code = models.CharField(_('code'), max_length=2, unique=True, db_index=True)  # ISO 3166-1 alpha-2
    name = models.CharField(_('name'), max_length=100)
    phone_code = models.CharField(_('phone code'), max_length=10)
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name='countries'
    )
    tax_settings = models.JSONField(_('tax settings'), default=dict)
    address_format = models.JSONField(_('address format'), default=dict)
    is_supported = models.BooleanField(_('supported'), default=True)
    
    class Meta:
        verbose_name = _('country')
        verbose_name_plural = _('countries')
        ordering = ['name']

class Plan(BaseModel):
    """
    Planos disponíveis no sistema
    """
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'))
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    billing_period = models.CharField(
        _('billing period'),
        max_length=20,
        choices=[
            ('monthly', _('Monthly')),
            ('yearly', _('Yearly')),
        ]
    )
    features = models.JSONField(_('features'), default=dict)
    limits = models.JSONField(_('limits'), default=dict)
    is_public = models.BooleanField(_('public'), default=True)
    sort_order = models.IntegerField(_('sort order'), default=0)
    
    class Meta:
        verbose_name = _('plan')
        verbose_name_plural = _('plans')
        ordering = ['sort_order', 'price']

class Module(BaseModel):
    """
    Módulos disponíveis no sistema
    """
    code = models.CharField(_('code'), max_length=100, unique=True, db_index=True)
    # ... outros campos ...
    name = models.CharField(_('name'), max_length=200)
    description = models.TextField(_('description'))
    type = models.CharField(
        _('type'),
        max_length=50,
        choices=[
            ('core', _('Core')),
            ('addon', _('Add-on')),
            ('integration', _('Integration')),
        ]
    )
    dependencies = models.JSONField(_('dependencies'), default=list)
    settings_schema = models.JSONField(_('settings schema'), default=dict)
    version = models.CharField(_('version'), max_length=50)
    is_required = models.BooleanField(_('required'), default=False)
    
    class Meta:
        verbose_name = _('module')
        verbose_name_plural = _('modules')
        ordering = ['code']

class AuditLog(BaseModel):
    """
    Log de auditoria para todas as ações importantes
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs'
    )
    action = models.CharField(_('action'), max_length=50)
    entity_type = models.CharField(_('entity type'), max_length=100)
    entity_id = models.UUIDField(_('entity id'))
    changes = models.JSONField(_('changes'), default=dict)
    ip_address = models.GenericIPAddressField(_('IP address'))
    user_agent = models.TextField(_('user agent'), blank=True)
    
    class Meta:
        verbose_name = _('audit log')
        verbose_name_plural = _('audit logs')
        ordering = ['-created_at']

class Notification(BaseModel):
    """
    Sistema de notificações
    """
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    type = models.CharField(_('type'), max_length=100)
    title = models.CharField(_('title'), max_length=200)
    message = models.TextField(_('message'))
    data = models.JSONField(_('data'), default=dict)
    read = models.BooleanField(_('read'), default=False)
    read_at = models.DateTimeField(_('read at'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'read']),
        ]