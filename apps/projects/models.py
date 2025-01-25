from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel
from companies.models import Company, CompanyUser
from commerce.models import Customer

class Project(BaseModel):
    """Projeto da empresa"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='projects')
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='projects')
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(
        max_length=50,
        choices=[
            ('planning', _('Planning')),
            ('in_progress', _('In Progress')),
            ('on_hold', _('On Hold')),
            ('completed', _('Completed')),
            ('cancelled', _('Cancelled')),
        ]
    )
    priority = models.IntegerField(
        choices=[
            (1, _('Low')),
            (2, _('Medium')),
            (3, _('High')),
            (4, _('Critical')),
        ]
    )
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    actual_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))
    team_members = models.ManyToManyField(CompanyUser, through='ProjectMember')
    documents = models.JSONField(default=list)
    custom_fields = models.JSONField(default=dict)

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['company', 'status']),
            models.Index(fields=['start_date', 'end_date']),
        ]
        
    def clean(self):
            if self.end_date <= self.start_date:
                raise ValidationError(_("End date must be after start date."))

class ProjectMember(BaseModel):
    """Membro da equipe do projeto"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(CompanyUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    responsibilities = models.TextField()
    allocation_percentage = models.IntegerField(default=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        unique_together = ['project', 'user']

class ProjectPhase(BaseModel):
    """Fase do projeto"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='phases')
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(
        max_length=50,
        choices=[
            ('planned', _('Planned')),
            ('in_progress', _('In Progress')),
            ('completed', _('Completed')),
            ('delayed', _('Delayed')),
        ]
    )
    completion_percentage = models.IntegerField(default=0)
    deliverables = models.JSONField(default=list)
    dependencies = models.ManyToManyField('self', symmetrical=False, blank=True)

class ProjectTask(BaseModel):
    """Tarefa do projeto"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    phase = models.ForeignKey(ProjectPhase, on_delete=models.CASCADE, related_name='tasks', null=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(CompanyUser, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks')
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()
    completed_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('todo', _('To Do')),
            ('in_progress', _('In Progress')),
            ('review', _('In Review')),
            ('completed', _('Completed')),
            ('blocked', _('Blocked')),
        ]
    )
    priority = models.IntegerField(
        choices=[
            (1, _('Low')),
            (2, _('Medium')),
            (3, _('High')),
            (4, _('Urgent')),
        ]
    )
    estimated_hours = models.DecimalField(max_digits=6, decimal_places=2)
    actual_hours = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0'))
    dependencies = models.ManyToManyField('self', symmetrical=False, blank=True)
    attachments = models.JSONField(default=list)
    tags = models.JSONField(default=list)

    class Meta:
        verbose_name = _('Project Task')
        verbose_name_plural = _('Project Tasks')
        ordering = ['due_date', 'priority']
        indexes = [
            models.Index(fields=['project', 'status']),
            models.Index(fields=['start_date', 'due_date']),
        ]

    def clean(self):
        if self.due_date <= self.start_date:
            raise ValidationError(_("Due date must be after start date."))
        if self.phase and (self.start_date < self.phase.start_date or self.due_date > self.phase.end_date):
            raise ValidationError(_("Task dates must be within phase dates."))

class ProjectResource(BaseModel):
    """Recursos alocados ao projeto"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='resources')
    resource_type = models.CharField(
        max_length=50,
        choices=[
            ('equipment', _('Equipment')),
            ('material', _('Material')),
            ('vehicle', _('Vehicle')),
            ('tool', _('Tool')),
        ]
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    allocation_start = models.DateTimeField()
    allocation_end = models.DateTimeField()
    status = models.CharField(
        max_length=50,
        choices=[
            ('available', _('Available')),
            ('in_use', _('In Use')),
            ('maintenance', _('In Maintenance')),
            ('reserved', _('Reserved')),
        ]
    )
    specifications = models.JSONField(default=dict)
    maintenance_history = models.JSONField(default=list)

class ProjectIssue(BaseModel):
    """Problemas/questões do projeto"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    reported_by = models.ForeignKey(CompanyUser, on_delete=models.SET_NULL, null=True, related_name='reported_issues')
    assigned_to = models.ForeignKey(CompanyUser, on_delete=models.SET_NULL, null=True, related_name='assigned_issues')
    title = models.CharField(max_length=200)
    description = models.TextField()
    issue_type = models.CharField(
        max_length=50,
        choices=[
            ('bug', _('Bug')),
            ('feature', _('Feature Request')),
            ('risk', _('Risk')),
            ('blocker', _('Blocker')),
            ('question', _('Question')),
        ]
    )
    priority = models.IntegerField(
        choices=[
            (1, _('Low')),
            (2, _('Medium')),
            (3, _('High')),
            (4, _('Critical')),
        ]
    )
    status = models.CharField(
        max_length=50,
        choices=[
            ('open', _('Open')),
            ('in_progress', _('In Progress')),
            ('resolved', _('Resolved')),
            ('closed', _('Closed')),
            ('reopened', _('Reopened')),
        ]
    )
    resolution = models.TextField(blank=True)
    due_date = models.DateTimeField(null=True)
    resolved_date = models.DateTimeField(null=True)
    attachments = models.JSONField(default=list)
    tags = models.JSONField(default=list)

    class Meta:
        verbose_name = _('Project Issue')
        verbose_name_plural = _('Project Issues')
        ordering = ['-created_at']

class ProjectTimeEntry(BaseModel):
    """Registro de horas trabalhadas"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='time_entries')
    task = models.ForeignKey(ProjectTask, on_delete=models.SET_NULL, null=True, related_name='time_entries')
    user = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, related_name='time_entries')
    date = models.DateField()
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    billable = models.BooleanField(default=True)
    billing_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        CompanyUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='approved_time_entries'
    )
    tags = models.JSONField(default=list)

    class Meta:
        verbose_name = _('Time Entry')
        verbose_name_plural = _('Time Entries')
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['project', 'user', 'date']),
        ]

    def clean(self):
        if self.hours <= 0:
            raise ValidationError(_("Hours must be greater than zero."))
        if self.date < self.project.start_date or self.date > self.project.end_date:
            raise ValidationError(_("Time entry date must be within project dates."))