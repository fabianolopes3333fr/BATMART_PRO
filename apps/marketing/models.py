from decimal import Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel
from companies.models import Company, CompanyUser
from commerce.models import Customer

class MarketingCampaign(BaseModel):
    """Campanha de marketing"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='marketing_campaigns')
    content = models.ManyToManyField('ContentManagement', related_name='campaigns', blank=True)

    name = models.CharField(max_length=200)
    description = models.TextField()
    campaign_type = models.CharField(
        max_length=50,
        choices=[
            ('email', _('Email')),
            ('social', _('Social Media')),
            ('ads', _('Paid Ads')),
            ('sms', _('SMS')),
            ('print', _('Print')),
            ('event', _('Event')),
        ]
    )
    status = models.CharField(
        max_length=50,
        choices=[
            ('draft', _('Draft')),
            ('scheduled', _('Scheduled')),
            ('active', _('Active')),
            ('paused', _('Paused')),
            ('completed', _('Completed')),
            ('cancelled', _('Cancelled')),
        ]
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    actual_spend = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))
    target_audience = models.JSONField(default=dict)
    goals = models.JSONField(default=dict)
    metrics = models.JSONField(default=dict)
    channels = models.JSONField(default=list)
    created_by = models.ForeignKey(CompanyUser, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = _('Marketing Campaign')
        verbose_name_plural = _('Marketing Campaigns')

class EmailCampaign(BaseModel):
    """Campanha de email marketing"""
    campaign = models.ForeignKey(MarketingCampaign, on_delete=models.CASCADE, related_name='email_campaigns')
    subject = models.CharField(max_length=200)
    preview_text = models.CharField(max_length=200)
    content_html = models.TextField()
    content_text = models.TextField()
    sender_name = models.CharField(max_length=100)
    sender_email = models.EmailField()
    recipient_list = models.JSONField(default=list)
    recipients = models.ManyToManyField(Customer, related_name='received_email_campaigns', blank=True)
    scheduled_time = models.DateTimeField()
    sent_time = models.DateTimeField(null=True, blank=True)
    opens = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    bounces = models.IntegerField(default=0)
    unsubscribes = models.IntegerField(default=0)
    status = models.CharField(
        max_length=50,
        choices=[
            ('draft', _('Draft')),
            ('scheduled', _('Scheduled')),
            ('sending', _('Sending')),
            ('sent', _('Sent')),
            ('failed', _('Failed')),
        ]
    )

class MarketingAutomation(BaseModel):
    """Automação de marketing"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='marketing_automations')
    name = models.CharField(max_length=200)
    description = models.TextField()
    trigger_type = models.CharField(
        max_length=50,
        choices=[
            ('event', _('Event Based')),
            ('schedule', _('Schedule Based')),
            ('behavior', _('Behavior Based')),
        ]
    )
    total_executions = models.IntegerField(default=0)
    last_execution = models.DateTimeField(null=True, blank=True)
    affected_customers = models.ManyToManyField(Customer, related_name='affected_by_automations', blank=True)

    trigger_conditions = models.JSONField(default=dict)
    actions = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    metrics = models.JSONField(default=dict)

class ContentManagement(BaseModel):
    """Gestão de conteúdo de marketing"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='marketing_content')
    title = models.CharField(max_length=200)
    content_type = models.CharField(
        max_length=50,
        choices=[
            ('blog', _('Blog Post')),
            ('social', _('Social Media Post')),
            ('email', _('Email Content')),
            ('landing', _('Landing Page')),
            ('ad', _('Advertisement')),
        ]
    )
    content = models.TextField()
    meta_description = models.TextField(blank=True)
    keywords = models.JSONField(default=list)
    author = models.ForeignKey(CompanyUser, on_delete=models.SET_NULL, null=True)
    publish_date = models.DateTimeField(null=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('draft', _('Draft')),
            ('review', _('In Review')),
            ('approved', _('Approved')),
            ('published', _('Published')),
            ('archived', _('Archived')),
        ]
    )
    categories = models.JSONField(default=list)
    tags = models.JSONField(default=list)
    featured_image = models.JSONField(default=dict)
    seo_settings = models.JSONField(default=dict)

class LeadManagement(BaseModel):
    """Gestão de leads"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='leads')
    source = models.CharField(max_length=100)
    campaign = models.ForeignKey(MarketingCampaign, on_delete=models.SET_NULL, null=True)
    contact_info = models.JSONField()
    status = models.CharField(
        max_length=50,
        choices=[
            ('new', _('New')),
            ('contacted', _('Contacted')),
            ('qualified', _('Qualified')),
            ('converted', _('Converted')),
            ('lost', _('Lost')),
        ]
    )
    score = models.IntegerField(default=0)
    assigned_to = models.ForeignKey(CompanyUser, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    conversion_path = models.JSONField(default=list)
    interactions = models.JSONField(default=list)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads')


class MarketingMetrics(BaseModel):
    """Métricas de marketing"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='marketing_metrics')
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    metrics_type = models.CharField(
        max_length=50,
        choices=[
            ('campaign', _('Campaign Metrics')),
            ('website', _('Website Analytics')),
            ('social', _('Social Media Metrics')),
            ('email', _('Email Metrics')),
            ('lead', _('Lead Generation')),
        ]
    )
    metrics_data = models.JSONField()
    source = models.CharField(max_length=100)
    annotations = models.JSONField(default=dict)
    is_processed = models.BooleanField(default=False)