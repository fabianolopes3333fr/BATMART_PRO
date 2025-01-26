from django import forms
from django.utils.translation import gettext_lazy as _
from .models import FinancialAccount, Transaction, Invoice, Budget, Expense

class FinancialAccountForm(forms.ModelForm):
    class Meta:
        model = FinancialAccount
        fields = ['name', 'account_type', 'currency', 'current_balance', 'available_balance',
                  'bank_name', 'account_number', 'routing_number', 'is_active']
        labels = {
            'name': _('Account Name'),  # FR: Nom du compte
            'account_type': _('Account Type'),  # FR: Type de compte
            'currency': _('Currency'),  # FR: Devise
            'current_balance': _('Current Balance'),  # FR: Solde actuel
            'available_balance': _('Available Balance'),  # FR: Solde disponible
            'bank_name': _('Bank Name'),  # FR: Nom de la banque
            'account_number': _('Account Number'),  # FR: Numéro de compte
            'routing_number': _('Routing Number'),  # FR: Numéro de routage
            'is_active': _('Active'),  # FR: Actif
        }
        help_texts = {
            'name': _('Enter the name of the financial account'),  # FR: Entrez le nom du compte financier
            'account_type': _('Select the type of financial account'),  # FR: Sélectionnez le type de compte financier
            'currency': _('Enter the 3-letter ISO currency code'),  # FR: Entrez le code ISO à 3 lettres de la devise
            'current_balance': _('Enter the current balance of the account'),  # FR: Entrez le solde actuel du compte
            'available_balance': _('Enter the available balance of the account'),  # FR: Entrez le solde disponible du compte
            'bank_name': _('Enter the name of the bank (optional)'),  # FR: Entrez le nom de la banque (facultatif)
            'account_number': _('Enter the account number (optional)'),  # FR: Entrez le numéro de compte (facultatif)
            'routing_number': _('Enter the routing number (optional)'),  # FR: Entrez le numéro de routage (facultatif)
            'is_active': _('Is this account currently active?'),  # FR: Ce compte est-il actuellement actif ?
        }
        error_messages = {
            'currency': {
                'max_length': _('Currency must be a 3-letter ISO code.'),  # FR: La devise doit être un code ISO à 3 lettres.
            },
        }

    def clean(self):
        cleaned_data = super().clean()
        current_balance = cleaned_data.get('current_balance')
        available_balance = cleaned_data.get('available_balance')

        if current_balance is not None and available_balance is not None:
            if available_balance > current_balance:
                raise forms.ValidationError(_("Available balance cannot be greater than current balance."))
                # FR: Le solde disponible ne peut pas être supérieur au solde actuel.

        return cleaned_data
    def clean_currency(self):
        currency = self.cleaned_data['currency']
        if len(currency) != 3:
            raise forms.ValidationError(_("Currency must be a 3-letter ISO code."))
            # FR: La devise doit être un code ISO à 3 lettres.
        return currency.upper()
    


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['account', 'transaction_type', 'amount', 'currency', 'description', 
                    'category', 'date', 'status', 'reference_number', 'payment_method']
        labels = {
            'account': _('Account'),  # FR: Compte
            'transaction_type': _('Transaction Type'),  # FR: Type de transaction
            'amount': _('Amount'),  # FR: Montant
            'currency': _('Currency'),  # FR: Devise
            'description': _('Description'),  # FR: Description
            'category': _('Category'),  # FR: Catégorie
            'date': _('Date'),  # FR: Date
            'status': _('Status'),  # FR: Statut
            'reference_number': _('Reference Number'),  # FR: Numéro de référence
            'payment_method': _('Payment Method'),  # FR: Méthode de paiement
        }
        help_texts = {
            'account': _('Select the account for this transaction'),  # FR: Sélectionnez le compte pour cette transaction
            'transaction_type': _('Choose the type of transaction'),  # FR: Choisissez le type de transaction
            'amount': _('Enter the transaction amount'),  # FR: Entrez le montant de la transaction
            'currency': _('Enter the 3-letter ISO currency code'),  # FR: Entrez le code ISO à 3 lettres de la devise
            'description': _('Provide a brief description of the transaction'),  # FR: Fournissez une brève description de la transaction
            'category': _('Select the category for this transaction'),  # FR: Sélectionnez la catégorie pour cette transaction
            'date': _('Enter the date of the transaction'),  # FR: Entrez la date de la transaction
            'status': _('Select the current status of the transaction'),  # FR: Sélectionnez le statut actuel de la transaction
            'reference_number': _('Enter a reference number if applicable'),  # FR: Entrez un numéro de référence si applicable
            'payment_method': _('Select the payment method used'),  # FR: Sélectionnez la méthode de paiement utilisée
        }
        error_messages = {
            'amount': {
                'invalid': _('Please enter a valid amount.'),  # FR: Veuillez entrer un montant valide.
            },
            'currency': {
                'max_length': _('Currency must be a 3-letter ISO code.'),  # FR: La devise doit être un code ISO à 3 lettres.
            },
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError(_("Amount must be greater than zero."))
            # FR: Le montant doit être supérieur à zéro.
        return amount

    def clean_currency(self):
        currency = self.cleaned_data['currency']
        if len(currency) != 3:
            raise forms.ValidationError(_("Currency must be a 3-letter ISO code."))
            # FR: La devise doit être un code ISO à 3 lettres.
        return currency.upper()

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        amount = cleaned_data.get('amount')

        if transaction_type and amount:
            if transaction_type == 'EXPENSE' and amount > 0:
                cleaned_data['amount'] = -abs(amount)
            elif transaction_type == 'INCOME' and amount < 0:
                cleaned_data['amount'] = abs(amount)

        return cleaned_data
    

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['company', 'customer', 'invoice_number', 'status', 'issue_date', 'due_date', 
                  'total_amount', 'tax_amount', 'discount_amount', 'notes', 'payment_terms']
        labels = {
            'company': _('Company'),  # FR: Entreprise
            'customer': _('Customer'),  # FR: Client
            'invoice_number': _('Invoice Number'),  # FR: Numéro de facture
            'status': _('Status'),  # FR: Statut
            'issue_date': _('Issue Date'),  # FR: Date d'émission
            'due_date': _('Due Date'),  # FR: Date d'échéance
            'total_amount': _('Total Amount'),  # FR: Montant total
            'tax_amount': _('Tax Amount'),  # FR: Montant des taxes
            'discount_amount': _('Discount Amount'),  # FR: Montant de la remise
            'notes': _('Notes'),  # FR: Notes
            'payment_terms': _('Payment Terms'),  # FR: Conditions de paiement
        }
        help_texts = {
            'invoice_number': _('Enter a unique invoice number'),  # FR: Entrez un numéro de facture unique
            'issue_date': _('Date when the invoice was issued'),  # FR: Date à laquelle la facture a été émise
            'due_date': _('Date when the payment is due'),  # FR: Date à laquelle le paiement est dû
            'total_amount': _('Total amount of the invoice'),  # FR: Montant total de la facture
            'tax_amount': _('Total tax amount'),  # FR: Montant total des taxes
            'discount_amount': _('Total discount amount'),  # FR: Montant total de la remise
            'notes': _('Additional notes or comments'),  # FR: Notes ou commentaires supplémentaires
            'payment_terms': _('Terms of payment for this invoice'),  # FR: Conditions de paiement pour cette facture
        }
        error_messages = {
            'invoice_number': {
                'unique': _('This invoice number already exists.'),  # FR: Ce numéro de facture existe déjà.
            },
            'total_amount': {
                'min_value': _('Total amount must be greater than zero.'),  # FR: Le montant total doit être supérieur à zéro.
            },
        }
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        issue_date = cleaned_data.get('issue_date')
        due_date = cleaned_data.get('due_date')

        if issue_date and due_date and due_date < issue_date:
            raise forms.ValidationError(_("Due date cannot be earlier than the issue date."))
            # FR: La date d'échéance ne peut pas être antérieure à la date d'émission.

        return cleaned_data

    def clean_total_amount(self):
        total_amount = self.cleaned_data['total_amount']
        if total_amount <= 0:
            raise forms.ValidationError(_("Total amount must be greater than zero."))
            # FR: Le montant total doit être supérieur à zéro.
        return total_amount

    def clean_tax_amount(self):
        tax_amount = self.cleaned_data['tax_amount']
        if tax_amount < 0:
            raise forms.ValidationError(_("Tax amount cannot be negative."))
            # FR: Le montant des taxes ne peut pas être négatif.
        return tax_amount

    def clean_discount_amount(self):
        discount_amount = self.cleaned_data['discount_amount']
        if discount_amount < 0:
            raise forms.ValidationError(_("Discount amount cannot be negative."))
            # FR: Le montant de la remise ne peut pas être négatif.
        return discount_amount
    

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['company', 'name', 'start_date', 'end_date', 'total_amount', 'category', 'description', 'status']
        labels = {
            'company': _('Company'),  # FR: Entreprise
            'name': _('Budget Name'),  # FR: Nom du budget
            'start_date': _('Start Date'),  # FR: Date de début
            'end_date': _('End Date'),  # FR: Date de fin
            'total_amount': _('Total Amount'),  # FR: Montant total
            'category': _('Category'),  # FR: Catégorie
            'description': _('Description'),  # FR: Description
            'status': _('Status'),  # FR: Statut
        }
        help_texts = {
            'name': _('Enter a name for this budget'),  # FR: Entrez un nom pour ce budget
            'start_date': _('The start date of the budget period'),  # FR: La date de début de la période budgétaire
            'end_date': _('The end date of the budget period'),  # FR: La date de fin de la période budgétaire
            'total_amount': _('The total amount allocated for this budget'),  # FR: Le montant total alloué pour ce budget
            'category': _('Select a category for this budget'),  # FR: Sélectionnez une catégorie pour ce budget
            'description': _('Provide a brief description of the budget'),  # FR: Fournissez une brève description du budget
            'status': _('Current status of the budget'),  # FR: Statut actuel du budget
        }
        error_messages = {
            'total_amount': {
                'min_value': _('Total amount must be greater than zero.'),  # FR: Le montant total doit être supérieur à zéro.
            },
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError(_("End date cannot be earlier than the start date."))
            # FR: La date de fin ne peut pas être antérieure à la date de début.

        return cleaned_data

    def clean_total_amount(self):
        total_amount = self.cleaned_data['total_amount']
        if total_amount <= 0:
            raise forms.ValidationError(_("Total amount must be greater than zero."))
            # FR: Le montant total doit être supérieur à zéro.
        return total_amount
    

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['company', 'amount', 'currency', 'date', 'category', 'description', 'payment_method', 'vendor', 'receipt']
        labels = {
            'company': _('Company'),  # FR: Entreprise
            'amount': _('Amount'),  # FR: Montant
            'currency': _('Currency'),  # FR: Devise
            'date': _('Date'),  # FR: Date
            'category': _('Category'),  # FR: Catégorie
            'description': _('Description'),  # FR: Description
            'payment_method': _('Payment Method'),  # FR: Méthode de paiement
            'vendor': _('Vendor'),  # FR: Fournisseur
            'receipt': _('Receipt'),  # FR: Reçu
        }
        help_texts = {
            'amount': _('Enter the expense amount'),  # FR: Entrez le montant de la dépense
            'currency': _('Enter the 3-letter ISO currency code'),  # FR: Entrez le code ISO à 3 lettres de la devise
            'date': _('Enter the date of the expense'),  # FR: Entrez la date de la dépense
            'category': _('Select the category for this expense'),  # FR: Sélectionnez la catégorie pour cette dépense
            'description': _('Provide a brief description of the expense'),  # FR: Fournissez une brève description de la dépense
            'payment_method': _('Select the payment method used'),  # FR: Sélectionnez la méthode de paiement utilisée
            'vendor': _('Enter the name of the vendor (optional)'),  # FR: Entrez le nom du fournisseur (facultatif)
            'receipt': _('Upload a receipt image (optional)'),  # FR: Téléchargez une image du reçu (facultatif)
        }
        error_messages = {
            'amount': {
                'invalid': _('Please enter a valid amount.'),  # FR: Veuillez entrer un montant valide.
            },
            'currency': {
                'max_length': _('Currency must be a 3-letter ISO code.'),  # FR: La devise doit être un code ISO à 3 lettres.
            },
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError(_("Amount must be greater than zero."))
            # FR: Le montant doit être supérieur à zéro.
        return amount

    def clean_currency(self):
        currency = self.cleaned_data['currency']
        if len(currency) != 3:
            raise forms.ValidationError(_("Currency must be a 3-letter ISO code."))
            # FR: La devise doit être un code ISO à 3 lettres.
        return currency.upper()

    def clean_receipt(self):
        receipt = self.cleaned_data.get('receipt')
        if receipt:
            if receipt.size > 5 * 1024 * 1024:  # 5 MB limit
                raise forms.ValidationError(_("The receipt file is too large. Maximum size is 5 MB."))
                # FR: Le fichier de reçu est trop volumineux. La taille maximale est de 5 Mo.
            allowed_types = ['image/jpeg', 'image/png', 'application/pdf']
            if receipt.content_type not in allowed_types:
                raise forms.ValidationError(_("Only JPEG, PNG, and PDF files are allowed."))
                # FR: Seuls les fichiers JPEG, PNG et PDF sont autorisés.
        return receipt