from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel
from companies.models import Company, CompanyUser



class Report(BaseModel):
    """Relatório personalizado"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='reports')
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    report_type = models.CharField(
        max_length=50,
        choices=[
            ('sales', _('Sales Report')),
            ('financial', _('Financial Report')),
            ('marketing', _('Marketing Report')),
            ('operations', _('Operations Report')),
            ('custom', _('Custom Report')),
        ]
    )
    template = models.JSONField()  # Configuração do template do relatório
    parameters = models.JSONField(default=dict)  # Parâmetros configuráveis
    schedule = models.JSONField(default=dict)  # Configuração de agendamento
    recipients = models.JSONField(default=list)  # Lista de destinatários
    last_generated = models.DateTimeField(null=True)
    created_by = models.ForeignKey(CompanyUser, on_delete=models.SET_NULL, null=True)

class ReportExecution(BaseModel):
    """Execução de relatório"""
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='executions')
    executed_by = models.ForeignKey(CompanyUser, on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('pending', _('Pending')),
            ('running', _('Running')),
            ('completed', _('Completed')),
            ('failed', _('Failed')),
        ]
    )
    parameters_used = models.JSONField()
    result_data = models.JSONField(null=True)
    error_message = models.TextField(blank=True)
    file_output = models.JSONField(default=dict)  # Informações do arquivo gerado

class Dashboard(BaseModel):
    """Dashboard personalizado"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='dashboards')
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    layout = models.JSONField()  # Configuração do layout
    widgets = models.JSONField(default=list)  # Lista de widgets
    permissions = models.JSONField(default=dict)  # Configurações de acesso
    is_default = models.BooleanField(default=False)
    created_by = models.ForeignKey(CompanyUser, on_delete=models.SET_NULL, null=True)

class Metric(BaseModel):
    """Métrica do sistema"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='metrics')
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    metric_type = models.CharField(
        max_length=50,
        choices=[
            ('count', _('Count')),
            ('sum', _('Sum')),
            ('average', _('Average')),
            ('percentage', _('Percentage')),
            ('custom', _('Custom')),
        ]
    )
    calculation = models.JSONField()  # Lógica de cálculo
    dimensions = models.JSONField(default=list)  # Dimensões para análise
    filters = models.JSONField(default=dict)  # Filtros aplicáveis
    update_frequency = models.CharField(
        max_length=50,
        choices=[
            ('realtime', _('Real-time')),
            ('hourly', _('Hourly')),
            ('daily', _('Daily')),
            ('weekly', _('Weekly')),
            ('monthly', _('Monthly')),
        ]
    )
    alerts = models.ManyToManyField('Alert', related_name='metrics', blank=True)
    last_updated = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)

class Alert(BaseModel):
    """Alerta baseado em métricas"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='alerts')
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE, related_name='alerts')
    condition = models.JSONField()  # Condição para disparo
    severity = models.CharField(
        max_length=50,
        choices=[
            ('info', _('Information')),
            ('warning', _('Warning')),
            ('critical', _('Critical')),
        ]
    )
    notification_channels = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    last_triggered = models.DateTimeField(null=True)
    
class DataExportManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('company', 'created_by')

class DataExport(BaseModel):
    """Exportação de dados"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='data_exports')
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    data_type = models.CharField(max_length=100)
    filters = models.JSONField(default=dict)
    format = models.CharField(
        max_length=50,
        choices=[
            ('csv', _('CSV')),
            ('excel', _('Excel')),
            ('json', _('JSON')),
            ('pdf', _('PDF')),
        ]
    )
    schedule = models.JSONField(default=dict)
    last_exported = models.DateTimeField(null=True)
    recipients = models.JSONField(default=list)
    created_by = models.ForeignKey(CompanyUser, on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to='exports/', null=True, blank=True)

    objects = DataExportManager()
    
    def clean(self):
        super().clean()
        errors = {}

        if not isinstance(self.filters, dict):
            errors['filters'] = _('Filters must be a dictionary.')
        if not isinstance(self.schedule, dict):
            errors['schedule'] = _('Schedule must be a dictionary.')
        if not isinstance(self.recipients, list):
            errors['recipients'] = _('Recipients must be a list.')

        if errors:
            raise ValidationError(errors)

    class Meta:
        indexes = [
            models.Index(fields=['company', 'name']),
            models.Index(fields=['last_exported']),
        ]