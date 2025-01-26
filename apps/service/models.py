from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel
from companies.models import Company, CompanyUser
from commerce.models import Customer
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Service(BaseModel):
    """Serviço oferecido pela empresa"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=200)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_minutes = models.IntegerField()
    pricing_model = models.JSONField(default=dict)
    availability_rules = models.JSONField(default=dict)
    booking_settings = models.JSONField(default=dict)
    requires_quote = models.BooleanField(default=False)
    qualification_required = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    categories = models.JSONField(default=list)

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    def __str__(self):
        return f"{self.name} - {self.company}"

class ServiceAppointment(BaseModel):
    """Agendamento de serviço"""
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='appointments')
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='appointments')
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField()
    STATUS_CHOICES = [
        ('scheduled', _('Scheduled')),
        ('confirmed', _('Confirmed')),
        ('in_progress', _('In Progress')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
        ('no_show', _('No Show')),
        # outros status...
    ]
    
    status = models.CharField(max_length=50,choices=STATUS_CHOICES)
    assigned_staff = models.ManyToManyField(CompanyUser, related_name='appointments')
    location_data = models.JSONField(default=dict)
    notes = models.TextField(blank=True)
    customer_requirements = models.JSONField(default=dict)
    service_report = models.JSONField(default=dict, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['service', 'scheduled_start', 'scheduled_end'],
                name='unique_service_appointment'
            )
        ]
class ServiceQuote(BaseModel):
    """Orçamento para serviço"""
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='quotes')
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='quotes')
    requirements = models.TextField()
    specifications = models.JSONField(default=dict)
    estimated_duration = models.IntegerField()  # em minutos
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2)
    valid_until = models.DateTimeField()
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('sent', _('Sent')),
        ('accepted', _('Accepted')),
        ('rejected', _('Rejected')),
        ('expired', _('Expired')),
        # outros status...
    ]
    
    status = models.CharField(max_length=50,choices=STATUS_CHOICES)
    notes = models.TextField(blank=True)
    terms_conditions = models.TextField()
    
    def is_expired(self):
        return timezone.now() > self.valid_until

class ServiceDeliverable(BaseModel):
    """Entregáveis do serviço"""
    appointment = models.ForeignKey(ServiceAppointment, on_delete=models.CASCADE, related_name='deliverables')
    name = models.CharField(max_length=200)
    description = models.TextField()
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('in_progress', _('In Progress')),
        ('completed', _('Completed')),
        ('accepted', _('Accepted')),
        ('rejected', _('Rejected')),
        # outros status...
    ]
    
    status = models.CharField(max_length=50,choices=STATUS_CHOICES)
    due_date = models.DateTimeField()
    completed_date = models.DateTimeField(null=True, blank=True)
    attachments = models.JSONField(default=list)
    verification_required = models.BooleanField(default=False)
    verification_status = models.JSONField(default=dict)

class ServiceReview(BaseModel):
    """Avaliação do serviço pelo cliente"""
    appointment = models.ForeignKey(ServiceAppointment, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='service_reviews')
    rating = models.IntegerField()  # 1-5
    review_text = models.TextField()
    attributes = models.JSONField(default=dict)  # pontualidade, qualidade, etc
    is_public = models.BooleanField(default=True)
    response = models.TextField(blank=True)  # resposta da empresa
    response_date = models.DateTimeField(null=True, blank=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )