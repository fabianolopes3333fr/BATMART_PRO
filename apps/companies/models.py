from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel, Plan, Module, Language

class Company(BaseModel):
    """Empresa cliente do sistema"""
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='owned_companies'
    )
    business_name = models.CharField(_('Business Name'), max_length=200)
    trading_name = models.CharField(_('Trading Name'), max_length=200)
    tax_id = models.CharField(_('Tax ID'), max_length=50, unique=True)
    registration_number = models.CharField(_('Registration Number'), max_length=50)
    legal_form = models.CharField(_('Legal Form'), max_length=100)
    contact_info = models.JSONField(_('Contact Info'), default=dict)
    addresses = models.JSONField(_('Addresses'), default=dict)
    primary_language = models.ForeignKey(
        Language,
        on_delete=models.PROTECT,
        related_name='primary_companies'
    )
    supported_languages = models.ManyToManyField(
        Language,
        related_name='supported_companies'
    )
    company_settings = models.JSONField(_('Company Settings'), default=dict)
    is_verified = models.BooleanField(_('Verified'), default=False)
    verification_status = models.CharField(
        _('Verification Status'),
        max_length=50,
        choices=[
            ('pending', _('Pending')),
            ('in_review', _('In Review')),
            ('verified', _('Verified')),
            ('rejected', _('Rejected')),
        ],
        default='pending'
    )
    account_status = models.CharField(
        _('Account Status'),
        max_length=50,
        choices=[
            ('active', _('Active')),
            ('suspended', _('Suspended')),
            ('cancelled', _('Cancelled')),
        ],
        default='active'
    )

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')
        ordering = ['business_name']

    def __str__(self):
        return self.business_name

class Subscription(BaseModel):
    """Assinatura de uma empresa"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    auto_renew = models.BooleanField(default=True)

    status = models.CharField(
        max_length=50,
        choices=[
            ('active', _('Active')),
            ('trial', _('Trial')),
            ('past_due', _('Past Due')),
            ('cancelled', _('Cancelled')),
            ('expired', _('Expired')),
        ]
    )
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle = models.CharField(
        max_length=20,
        choices=[
            ('monthly', _('Monthly')),
            ('yearly', _('Yearly')),
        ]
    )
    payment_info = models.JSONField(default=dict)
    usage_metrics = models.JSONField(default=dict)
    last_billing_date = models.DateTimeField(null=True)
    cancel_reason = models.TextField(blank=True)

    class Meta:
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')
        get_latest_by = 'created_at'

class CompanyUser(BaseModel):
    """Usuário associado a uma empresa"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='users')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    contact_info = models.JSONField(default=dict)
    status = models.CharField(
        max_length=50,
        choices=[
            ('active', _('Active')),
            ('inactive', _('Inactive')),
            ('pending', _('Pending Activation')),
        ],
        default='pending'
    )
    security_settings = models.JSONField(default=dict)
    notification_preferences = models.JSONField(default=dict)
    preferred_language = models.ForeignKey(
        Language,
        on_delete=models.SET_NULL,
        null=True,
        related_name='preferred_users'
    )
    access_level = models.CharField(
        max_length=50,
        choices=[
            ('admin', _('Admin')),
            ('manager', _('Manager')),
            ('staff', _('Staff')),
        ],
        default='staff'
    )

    class Meta:
        verbose_name = _('Company User')
        verbose_name_plural = _('Company Users')
        unique_together = ['company', 'user']

class CompanyModule(BaseModel):
    """Módulos ativos para uma empresa"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='modules')
    module = models.ForeignKey(Module, on_delete=models.PROTECT, related_name='company_modules')
    status = models.CharField(
        max_length=50,
        choices=[
            ('active', _('Active')),
            ('inactive', _('Inactive')),
            ('pending', _('Pending')),
            ('suspended', _('Suspended')),
        ]
    )
    activation_date = models.DateTimeField(null=True)
    module_settings = models.JSONField(default=dict)
    usage_statistics = models.JSONField(default=dict)
    version = models.CharField(max_length=50)
    last_used = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Company Module')
        verbose_name_plural = _('Company Modules')
        unique_together = ['company', 'module']

class CompanyStatusHistory(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=50)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    reason = models.TextField(blank=True)

    class Meta:
        verbose_name = _('Company Status History')
        verbose_name_plural = _('Company Status Histories')
        ordering = ['-created_at']