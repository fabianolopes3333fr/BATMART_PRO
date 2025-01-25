from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel
from companies.models import Company, CompanyUser
from commerce.models import Customer, Order

class FinancialAccount(BaseModel):
    """Conta financeira da empresa"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='financial_accounts')
    name = models.CharField(max_length=200)
    account_type = models.CharField(
        max_length=50,
        choices=[
            ('checking', _('Checking')),
            ('savings', _('Savings')),
            ('credit', _('Credit')),
            ('investment', _('Investment')),
        ]
    )
    currency = models.CharField(max_length=3)  # ISO currency code
    current_balance = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    available_balance = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    bank_name = models.CharField(max_length=200, blank=True)
    account_number = models.CharField(max_length=100, blank=True)
    routing_number = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    last_reconciliation = models.DateTimeField(null=True)
    settings = models.JSONField(default=dict)

    
    class Meta:
        indexes = [
            models.Index(fields=['company', 'is_active']),
        ]


class Transaction(BaseModel):
    """Transação financeira"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='transactions')
    account = models.ForeignKey(FinancialAccount, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(
        max_length=50,
        choices=[
            ('income', _('Income')),
            ('expense', _('Expense')),
            ('transfer', _('Transfer')),
            ('refund', _('Refund')),
        ]
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=6, default=Decimal('1.0'), validators=[MinValueValidator(0)])
    date = models.DateTimeField()
    description = models.TextField()
    category = models.CharField(max_length=100)
    status = models.CharField(
        max_length=50,
        choices=[
            ('pending', _('Pending')),
            ('completed', _('Completed')),
            ('failed', _('Failed')),
            ('cancelled', _('Cancelled')),
        ]
    )
    reference_number = models.CharField(max_length=100, blank=True)
    related_order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name='transactions')
    invoice = models.ForeignKey('Invoice', on_delete=models.SET_NULL, null=True, related_name='transactions')
    metadata = models.JSONField(default=dict)
    tags = models.JSONField(default=list)

    class Meta:
        indexes = [
            models.Index(fields=['company', 'date']),
            models.Index(fields=['reference_number']),
        ]

class Invoice(BaseModel):
    """Fatura para cliente"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='invoices')
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='invoices')
    invoice_number = models.CharField(max_length=50, unique=True, db_index=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name='invoices')
    issue_date = models.DateTimeField()
    due_date = models.DateTimeField()
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    tax_total = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    total = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(
        max_length=50,
        choices=[
            ('draft', _('Draft')),
            ('sent', _('Sent')),
            ('paid', _('Paid')),
            ('partial', _('Partially Paid')),
            ('overdue', _('Overdue')),
            ('cancelled', _('Cancelled')),
        ]
    )
    payment_terms = models.TextField()
    notes = models.TextField(blank=True)
    items = models.JSONField(default=list)
    payments = models.JSONField(default=list)

    class Meta:
        indexes = [
            models.Index(fields=['company', 'issue_date']),
            models.Index(fields=['invoice_number']),
        ]

    def clean(self):
        if self.due_date < self.issue_date:
            raise ValidationError(_("Due date cannot be earlier than issue date."))
        if self.total != self.subtotal + self.tax_total:
            raise ValidationError(_("Total must be equal to subtotal plus tax total."))

class Budget(BaseModel):
    """Orçamento da empresa"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='budgets')
    name = models.CharField(max_length=200)
    period_start = models.DateField()
    period_end = models.DateField()
    total_budget = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    categories = models.JSONField(default=dict)  # Categorias e valores alocados
    actual_spend = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0'), validators=[MinValueValidator(0)])
    status = models.CharField(
        max_length=50,
        choices=[
            ('draft', _('Draft')),
            ('active', _('Active')),
            ('closed', _('Closed')),
        ]
    )
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        CompanyUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_budgets'
    )

    class Meta:
        indexes = [
            models.Index(fields=['company', 'period_start', 'period_end']),
        ]

    def clean(self):
        if self.period_end < self.period_start:
            raise ValidationError(_("End period cannot be earlier than start period."))

class Expense(BaseModel):
    """Despesa da empresa"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='expenses')
    description = models.TextField()
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    category = models.CharField(max_length=100)
    date = models.DateTimeField()
    payment_method = models.CharField(max_length=100)
    status = models.CharField(
        max_length=50,
        choices=[
            ('pending', _('Pending')),
            ('approved', _('Approved')),
            ('rejected', _('Rejected')),
            ('paid', _('Paid')),
        ]
    )
    submitted_by = models.ForeignKey(
        CompanyUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='submitted_expenses'
    )
    approved_by = models.ForeignKey(
        CompanyUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='approved_expenses'
    )
    receipt = models.JSONField(default=dict)  # Informações do recibo/nota fiscal
    reimbursable = models.BooleanField(default=False)
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.SET_NULL,
        null=True,
        related_name='expenses'
    )
    tags = models.JSONField(default=list)

    class Meta:
        indexes = [
            models.Index(fields=['company', 'date']),
            models.Index(fields=['category']),
        ]