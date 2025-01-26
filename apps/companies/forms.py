from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Company, Subscription, CompanyUser, CompanyModule,  CompanyStatusHistory
from django.contrib.auth import get_user_model
from django.forms.widgets import JSONInput

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['owner', 'business_name', 'trading_name', 'tax_id', 'registration_number', 
                  'legal_form', 'contact_info', 'addresses', 'primary_language', 
                  'supported_languages', 'company_settings', 'is_verified', 
                  'verification_status', 'account_status']
        
        widgets = {
            'contact_info': forms.JSONInput(),
            'addresses': forms.JSONInput(),
            'company_settings': forms.JSONInput(),
            'supported_languages': forms.CheckboxSelectMultiple(),
        }

        labels = {
            'owner': _('Owner'),
            'business_name': _('Business Name'),
            'trading_name': _('Trading Name'),
            'tax_id': _('Tax ID'),
            'registration_number': _('Registration Number'),
            'legal_form': _('Legal Form'),
            'contact_info': _('Contact Info'),
            'addresses': _('Addresses'),
            'primary_language': _('Primary Language'),
            'supported_languages': _('Supported Languages'),
            'company_settings': _('Company Settings'),
            'is_verified': _('Verified'),
            'verification_status': _('Verification Status'),
            'account_status': _('Account Status'),
        }

        error_messages = {
            'business_name': {
                'required': _('Business name is required.'),
                'max_length': _('Business name cannot exceed 200 characters.'),
            },
            'tax_id': {
                'required': _('Tax ID is required.'),
                'unique': _('This Tax ID is already in use.'),
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['owner'].widget.attrs['class'] = 'select2'
        self.fields['primary_language'].widget.attrs['class'] = 'select2'
        self.fields['supported_languages'].widget.attrs['class'] = 'select2-multiple'

    def clean_tax_id(self):
        tax_id = self.cleaned_data.get('tax_id')
        if tax_id:
            # Add any specific validation for tax_id if needed
            pass
        return tax_id

# Translations for French
_ = lambda s: s

fr_translations = {
    'Owner': _('Propriétaire'),
    'Business Name': _('Nom de l\'entreprise'),
    'Trading Name': _('Nom commercial'),
    'Tax ID': _('Numéro d\'identification fiscale'),
    'Registration Number': _('Numéro d\'enregistrement'),
    'Legal Form': _('Forme juridique'),
    'Contact Info': _('Informations de contact'),
    'Addresses': _('Adresses'),
    'Primary Language': _('Langue principale'),
    'Supported Languages': _('Langues prises en charge'),
    'Company Settings': _('Paramètres de l\'entreprise'),
    'Verified': _('Vérifié'),
    'Verification Status': _('Statut de vérification'),
    'Account Status': _('Statut du compte'),
    'Business name is required.': _('Le nom de l\'entreprise est requis.'),
    'Business name cannot exceed 200 characters.': _('Le nom de l\'entreprise ne peut pas dépasser 200 caractères.'),
    'Tax ID is required.': _('Le numéro d\'identification fiscale est requis.'),
    'This Tax ID is already in use.': _('Ce numéro d\'identification fiscale est déjà utilisé.'),
}


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['company', 'plan', 'start_date', 'end_date', 'auto_renew', 'status',
                  'current_price', 'billing_cycle', 'payment_info', 'usage_metrics',
                  'last_billing_date', 'cancel_reason']
        
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'payment_info': forms.JSONInput(),
            'usage_metrics': forms.JSONInput(),
            'last_billing_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

        labels = {
            'company': _('Company'),
            'plan': _('Plan'),
            'start_date': _('Start Date'),
            'end_date': _('End Date'),
            'auto_renew': _('Auto Renew'),
            'status': _('Status'),
            'current_price': _('Current Price'),
            'billing_cycle': _('Billing Cycle'),
            'payment_info': _('Payment Info'),
            'usage_metrics': _('Usage Metrics'),
            'last_billing_date': _('Last Billing Date'),
            'cancel_reason': _('Cancel Reason'),
        }

        error_messages = {
            'company': {
                'required': _('Company is required.'),
            },
            'plan': {
                'required': _('Plan is required.'),
            },
            'start_date': {
                'required': _('Start date is required.'),
            },
            'current_price': {
                'required': _('Current price is required.'),
                'invalid': _('Please enter a valid price.'),
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].widget.attrs['class'] = 'select2'
        self.fields['plan'].widget.attrs['class'] = 'select2'
        self.fields['status'].widget.attrs['class'] = 'select2'
        self.fields['billing_cycle'].widget.attrs['class'] = 'select2'

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date <= start_date:
            raise forms.ValidationError(_('End date must be after start date.'))

        return cleaned_data

# Translations for French
_ = lambda s: s

fr_translations = {
    'Company': _('Entreprise'),
    'Plan': _('Plan'),
    'Start Date': _('Date de début'),
    'End Date': _('Date de fin'),
    'Auto Renew': _('Renouvellement automatique'),
    'Status': _('Statut'),
    'Current Price': _('Prix actuel'),
    'Billing Cycle': _('Cycle de facturation'),
    'Payment Info': _('Informations de paiement'),
    'Usage Metrics': _('Métriques d\'utilisation'),
    'Last Billing Date': _('Dernière date de facturation'),
    'Cancel Reason': _('Raison d\'annulation'),
    'Company is required.': _('L\'entreprise est requise.'),
    'Plan is required.': _('Le plan est requis.'),
    'Start date is required.': _('La date de début est requise.'),
    'Current price is required.': _('Le prix actuel est requis.'),
    'Please enter a valid price.': _('Veuillez entrer un prix valide.'),
    'End date must be after start date.': _('La date de fin doit être postérieure à la date de début.'),
}



class CompanyUserForm(forms.ModelForm):
    class Meta:
        model = CompanyUser
        fields = ['company', 'user', 'job_title', 'department', 'contact_info', 'status',
                  'security_settings', 'notification_preferences', 'preferred_language',
                  'access_level']
        
        widgets = {
            'contact_info': forms.JSONInput(),
            'security_settings': forms.JSONInput(),
            'notification_preferences': forms.JSONInput(),
        }

        labels = {
            'company': _('Company'),
            'user': _('User'),
            'job_title': _('Job Title'),
            'department': _('Department'),
            'contact_info': _('Contact Info'),
            'status': _('Status'),
            'security_settings': _('Security Settings'),
            'notification_preferences': _('Notification Preferences'),
            'preferred_language': _('Preferred Language'),
            'access_level': _('Access Level'),
        }

        error_messages = {
            'company': {
                'required': _('Company is required.'),
            },
            'user': {
                'required': _('User is required.'),
            },
            'job_title': {
                'required': _('Job title is required.'),
                'max_length': _('Job title cannot exceed 100 characters.'),
            },
            'department': {
                'required': _('Department is required.'),
                'max_length': _('Department cannot exceed 100 characters.'),
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].widget.attrs['class'] = 'select2'
        self.fields['user'].widget.attrs['class'] = 'select2'
        self.fields['preferred_language'].widget.attrs['class'] = 'select2'
        self.fields['status'].widget.attrs['class'] = 'select2'
        self.fields['access_level'].widget.attrs['class'] = 'select2'

    def clean(self):
        cleaned_data = super().clean()
        company = cleaned_data.get('company')
        user = cleaned_data.get('user')

        if company and user:
            if CompanyUser.objects.filter(company=company, user=user).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(_('This user is already associated with the company.'))

        return cleaned_data

# Translations for French
_ = lambda s: s

fr_translations.update({
    'Company': _('Entreprise'),
    'User': _('Utilisateur'),
    'Job Title': _('Titre du poste'),
    'Department': _('Département'),
    'Contact Info': _('Informations de contact'),
    'Status': _('Statut'),
    'Security Settings': _('Paramètres de sécurité'),
    'Notification Preferences': _('Préférences de notification'),
    'Preferred Language': _('Langue préférée'),
    'Access Level': _('Niveau d\'accès'),
    'Company is required.': _('L\'entreprise est requise.'),
    'User is required.': _('L\'utilisateur est requis.'),
    'Job title is required.': _('Le titre du poste est requis.'),
    'Job title cannot exceed 100 characters.': _('Le titre du poste ne peut pas dépasser 100 caractères.'),
    'Department is required.': _('Le département est requis.'),
    'Department cannot exceed 100 characters.': _('Le département ne peut pas dépasser 100 caractères.'),
    'This user is already associated with the company.': _('Cet utilisateur est déjà associé à l\'entreprise.'),
})



class CompanyModuleForm(forms.ModelForm):
    class Meta:
        model = CompanyModule
        fields = ['company', 'module', 'status', 'activation_date', 'module_settings', 
                  'usage_statistics', 'version', 'last_used', 'is_active']
        
        widgets = {
            'activation_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'last_used': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'module_settings': forms.JSONInput(),
            'usage_statistics': forms.JSONInput(),
        }

        labels = {
            'company': _('Company'),
            'module': _('Module'),
            'status': _('Status'),
            'activation_date': _('Activation Date'),
            'module_settings': _('Module Settings'),
            'usage_statistics': _('Usage Statistics'),
            'version': _('Version'),
            'last_used': _('Last Used'),
            'is_active': _('Is Active'),
        }

        error_messages = {
            'company': {
                'required': _('Company is required.'),
            },
            'module': {
                'required': _('Module is required.'),
            },
            'status': {
                'required': _('Status is required.'),
            },
            'version': {
                'required': _('Version is required.'),
                'max_length': _('Version cannot exceed 50 characters.'),
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].widget.attrs['class'] = 'select2'
        self.fields['module'].widget.attrs['class'] = 'select2'
        self.fields['status'].widget.attrs['class'] = 'select2'

    def clean(self):
        cleaned_data = super().clean()
        company = cleaned_data.get('company')
        module = cleaned_data.get('module')

        if company and module:
            if CompanyModule.objects.filter(company=company, module=module).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(_('This module is already associated with the company.'))

        return cleaned_data

# Translations for French
_ = lambda s: s

fr_translations = {
    'Company': _('Entreprise'),
    'Module': _('Module'),
    'Status': _('Statut'),
    'Activation Date': _('Date d\'activation'),
    'Module Settings': _('Paramètres du module'),
    'Usage Statistics': _('Statistiques d\'utilisation'),
    'Version': _('Version'),
    'Last Used': _('Dernière utilisation'),
    'Is Active': _('Est actif'),
    'Company is required.': _('L\'entreprise est requise.'),
    'Module is required.': _('Le module est requis.'),
    'Status is required.': _('Le statut est requis.'),
    'Version is required.': _('La version est requise.'),
    'Version cannot exceed 50 characters.': _('La version ne peut pas dépasser 50 caractères.'),
    'This module is already associated with the company.': _('Ce module est déjà associé à l\'entreprise.'),
}



User = get_user_model()

class CompanyStatusHistoryForm(forms.ModelForm):
    class Meta:
        model = CompanyStatusHistory
        fields = ['company', 'status', 'changed_by', 'reason']

        widgets = {
            'reason': forms.Textarea(attrs={'rows': 4}),
        }

        labels = {
            'company': _('Company'),
            'status': _('Status'),
            'changed_by': _('Changed By'),
            'reason': _('Reason'),
        }

        error_messages = {
            'company': {
                'required': _('Company is required.'),
            },
            'status': {
                'required': _('Status is required.'),
                'max_length': _('Status cannot exceed 50 characters.'),
            },
            'changed_by': {
                'required': _('User who changed the status is required.'),
            },
        }

    def __init__(self, *args, **kwargs):
        STATUS_CHOICES = [
            ('active', _('Active')),
            ('inactive', _('Inactive')),
            ('pending', _('Pending')),
            ('suspended', _('Suspended')),
            ('cancelled', _('Cancelled')),
        # outros status...
        ]
        super().__init__(*args, **kwargs)
        self.fields['company'].widget.attrs['class'] = 'select2'
        self.fields['changed_by'].widget.attrs['class'] = 'select2'
        self.fields['status'].widget = forms.Select(choices=STATUS_CHOICES,)

    def clean_status(self):
        status = self.cleaned_data.get('status')
        if status not in dict(self.fields['status'].widget.choices):
            raise forms.ValidationError(_('Invalid status selected.'))
        return status

# Translations for French
_ = lambda s: s

fr_translations = {
    'Company': _('Entreprise'),
    'Status': _('Statut'),
    'Changed By': _('Modifié par'),
    'Reason': _('Raison'),
    'Company is required.': _('L\'entreprise est requise.'),
    'Status is required.': _('Le statut est requis.'),
    'Status cannot exceed 50 characters.': _('Le statut ne peut pas dépasser 50 caractères.'),
    'User who changed the status is required.': _('L\'utilisateur qui a modifié le statut est requis.'),
    'Invalid status selected.': _('Statut sélectionné invalide.'),
    'Active': _('Actif'),
    'Suspended': _('Suspendu'),
    'Cancelled': _('Annulé'),
}