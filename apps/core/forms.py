from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from .models import User, BaseModel, SystemConfiguration, Language, Currency, Country, Plan, Module, AuditLog, Notification

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'phone', 'locale', 'timezone')
        labels = {
            'email': _('Email'),
            'phone': _('Phone number'),
            'locale': _('Locale'),
            'timezone': _('Timezone'),
        }
        error_messages = {
            'email': {
                'unique': _('A user with that email already exists.'),
                'required': _('Email is required.'),
            },
            'phone': {
                'invalid': _('Enter a valid phone number.'),
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autofocus': True})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = self.Meta.model.objects.normalize_email(email)
        return email

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'phone', 'locale', 'timezone', 'profile_image', 'notification_settings')
        labels = {
            'email': _('Email'),
            'phone': _('Phone number'),
            'locale': _('Locale'),
            'timezone': _('Timezone'),
            'profile_image': _('Profile image'),
            'notification_settings': _('Notification settings'),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = self.Meta.model.objects.normalize_email(email)
        return email

# Translations for French
_ = lambda s: s
french_translations = {
    'Email': _('Adresse e-mail'),
    'Phone number': _('Numéro de téléphone'),
    'Locale': _('Paramètres régionaux'),
    'Timezone': _('Fuseau horaire'),
    'Profile image': _('Image de profil'),
    'Notification settings': _('Paramètres de notification'),
    'A user with that email already exists.': _('Un utilisateur avec cette adresse e-mail existe déjà.'),
    'Email is required.': _("L'adresse e-mail est requise."),
    'Enter a valid phone number.': _('Entrez un numéro de téléphone valide.'),
} 

class BaseModelForm(forms.ModelForm):
    class Meta:
        model = BaseModel
        fields = ['is_active', 'metadata']
        widgets = {
            'metadata': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'is_active': _('Active'),
            'metadata': _('Metadata'),
        }
        help_texts = {
            'is_active': _('Designates whether this item is currently active.'),
            'metadata': _('Additional data in JSON format.'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_active'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
        self.fields['metadata'].widget.attrs.update({'class': 'form-control'})

    def clean_metadata(self):
        metadata = self.cleaned_data.get('metadata')
        if metadata:
            try:
                import json
                json.loads(metadata)
            except json.JSONDecodeError:
                raise forms.ValidationError(_('Invalid JSON format for metadata.'))
        return metadata

# Translations for French
_ = lambda s: s
french_translations = {
    'Active': _('Actif'),
    'Metadata': _('Métadonnées'),
    'Designates whether this item is currently active.': _('Indique si cet élément est actuellement actif.'),
    'Additional data in JSON format.': _('Données supplémentaires au format JSON.'),
    'Invalid JSON format for metadata.': _('Format JSON invalide pour les métadonnées.'),
}


class SystemConfigurationForm(forms.ModelForm):
    class Meta:
        model = SystemConfiguration
        fields = ['key', 'value', 'value_type', 'description', 'is_editable']
        widgets = {
            'key': forms.TextInput(attrs={'class': 'form-control'}),
            'value': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'value_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_editable': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'key': _('Configuration Key'),
            'value': _('Configuration Value'),
            'value_type': _('Value Type'),
            'description': _('Description'),
            'is_editable': _('Editable'),
        }
        help_texts = {
            'key': _('Unique identifier for this configuration.'),
            'value': _('The value of the configuration.'),
            'value_type': _('The data type of the value.'),
            'description': _('A brief description of this configuration.'),
            'is_editable': _('Can this configuration be edited through the interface?'),
        }
        error_messages = {
            'key': {
                'unique': _('A configuration with this key already exists.'),
            },
        }

    def clean_value(self):
        value = self.cleaned_data.get('value')
        value_type = self.cleaned_data.get('value_type')
        if not value:  # Verifica se value é None ou vazio
            return value

        if value_type == 'boolean':
            if value.lower() not in ('true', 'false'):
                raise forms.ValidationError(_('Boolean value must be either "true" or "false".'))
        elif value_type == 'integer':
            try:
                int(value)
            except ValueError:
                raise forms.ValidationError(_('Please enter a valid integer.'))
        elif value_type == 'float':
            try:
                float(value)
            except ValueError:
                raise forms.ValidationError(_('Please enter a valid float number.'))
        elif value_type == 'json':
            try:
                import json
                json.loads(value)
            except json.JSONDecodeError:
                raise forms.ValidationError(_('Please enter a valid JSON.'))

        return value

# Translations for French
_ = lambda s: s
french_translations = {
    'Configuration Key': _('Clé de Configuration'),
    'Configuration Value': _('Valeur de Configuration'),
    'Value Type': _('Type de Valeur'),
    'Description': _('Description'),
    'Editable': _('Modifiable'),
    'Unique identifier for this configuration.': _('Identifiant unique pour cette configuration.'),
    'The value of the configuration.': _('La valeur de la configuration.'),
    'The data type of the value.': _('Le type de données de la valeur.'),
    'A brief description of this configuration.': _('Une brève description de cette configuration.'),
    'Can this configuration be edited through the interface?': _("Cette configuration peut-elle être modifiée via l'interface ?"),
    'A configuration with this key already exists.': _('Une configuration avec cette clé existe déjà.'),
    'Boolean value must be either "true" or "false".': _('La valeur booléenne doit être "true" ou "false".'),
    'Please enter a valid integer.': _('Veuillez entrer un nombre entier valide.'),
    'Please enter a valid float number.': _('Veuillez entrer un nombre décimal valide.'),
    'Please enter a valid JSON.': _('Veuillez entrer un JSON valide.'),
}


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['name', 'code', 'native_name', 'is_default', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'native_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': _('Language Name'),
            'code': _('Language Code'),
            'native_name': _('Native Name'),
            'is_default': _('Default Language'),
            'is_active': _('Active'),
        }
        help_texts = {
            'name': _('The name of the language in English.'),
            'code': _('The ISO 639-1 language code (e.g., "en" for English).'),
            'native_name': _('The name of the language in its native form.'),
            'is_default': _('Is this the default language for the system?'),
            'is_active': _('Is this language currently active in the system?'),
        }
        error_messages = {
            'code': {
                'unique': _('A language with this code already exists.'),
            },
        }

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if code:
            code = code.lower()
            if len(code) != 2:
                raise forms.ValidationError(_('Language code must be exactly 2 characters long.'))
        return code

    def clean(self):
        cleaned_data = super().clean()
        is_default = cleaned_data.get('is_default')
        is_active = cleaned_data.get('is_active')

        if is_default and not is_active:
            raise forms.ValidationError(_('The default language must be active.'))

        return cleaned_data

# Translations for French
_ = lambda s: s
french_translations = {
    'Language Name': _('Nom de la langue'),
    'Language Code': _('Code de la langue'),
    'Native Name': _('Nom natif'),
    'Default Language': _('Langue par défaut'),
    'Active': _('Actif'),
    'The name of the language in English.': _('Le nom de la langue en anglais.'),
    'The ISO 639-1 language code (e.g., "en" for English).': _('Le code de langue ISO 639-1 (par exemple, "fr" pour le français).'),
    'The name of the language in its native form.': _('Le nom de la langue dans sa forme native.'),
    'Is this the default language for the system?': _('Est-ce la langue par défaut du système ?'),
    'Is this language currently active in the system?': _('Cette langue est-elle actuellement active dans le système ?'),
    'A language with this code already exists.': _('Une langue avec ce code existe déjà.'),
    'Language code must be exactly 2 characters long.': _('Le code de langue doit comporter exactement 2 caractères.'),
    'The default language must be active.': _('La langue par défaut doit être active.'),
}


class CurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = ['name', 'code', 'symbol', 'decimal_places', 'is_default', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'symbol': forms.TextInput(attrs={'class': 'form-control'}),
            'decimal_places': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': _('Currency Name'),
            'code': _('Currency Code'),
            'symbol': _('Currency Symbol'),
            'decimal_places': _('Decimal Places'),
            'is_default': _('Default Currency'),
            'is_active': _('Active'),
        }
        help_texts = {
            'name': _('The full name of the currency.'),
            'code': _('The ISO 4217 currency code (e.g., "USD" for US Dollar).'),
            'symbol': _('The symbol used to represent the currency.'),
            'decimal_places': _('The number of decimal places for this currency.'),
            'is_default': _('Is this the default currency for the system?'),
            'is_active': _('Is this currency currently active in the system?'),
        }
        error_messages = {
            'code': {
                'unique': _('A currency with this code already exists.'),
            },
        }

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if code:
            code = code.upper()
            if len(code) != 3:
                raise forms.ValidationError(_('Currency code must be exactly 3 characters long.'))
        return code

    def clean_decimal_places(self):
        decimal_places = self.cleaned_data.get('decimal_places')
        if decimal_places is not None and (decimal_places < 0 or decimal_places > 10):
            raise forms.ValidationError(_('Decimal places must be between 0 and 10.'))
        return decimal_places

    def clean(self):
        cleaned_data = super().clean()
        is_default = cleaned_data.get('is_default')
        is_active = cleaned_data.get('is_active')

        if is_default and not is_active:
            raise forms.ValidationError(_('The default currency must be active.'))

        return cleaned_data

# Translations for French
_ = lambda s: s
french_translations = {
    'Currency Name': _('Nom de la devise'),
    'Currency Code': _('Code de la devise'),
    'Currency Symbol': _('Symbole de la devise'),
    'Decimal Places': _('Nombre de décimales'),
    'Default Currency': _('Devise par défaut'),
    'Active': _('Actif'),
    'The full name of the currency.': _('Le nom complet de la devise.'),
    'The ISO 4217 currency code (e.g., "USD" for US Dollar).': _('Le code de devise ISO 4217 (par exemple, "EUR" pour Euro).'),
    'The symbol used to represent the currency.': _('Le symbole utilisé pour représenter la devise.'),
    'The number of decimal places for this currency.': _('Le nombre de décimales pour cette devise.'),
    'Is this the default currency for the system?': _('Est-ce la devise par défaut du système ?'),
    'Is this currency currently active in the system?': _('Cette devise est-elle actuellement active dans le système ?'),
    'A currency with this code already exists.': _('Une devise avec ce code existe déjà.'),
    'Currency code must be exactly 3 characters long.': _('Le code de devise doit comporter exactement 3 caractères.'),
    'Decimal places must be between 0 and 10.': _('Le nombre de décimales doit être compris entre 0 et 10.'),
    'The default currency must be active.': _('La devise par défaut doit être active.'),
}


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['name', 'code', 'phone_code', 'currency', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_code': forms.TextInput(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': _('Country Name'),
            'code': _('Country Code'),
            'phone_code': _('Phone Code'),
            'currency': _('Currency'),
            'is_active': _('Active'),
        }
        help_texts = {
            'name': _('The full name of the country.'),
            'code': _('The ISO 3166-1 alpha-2 country code (e.g., "US" for United States).'),
            'phone_code': _('The international phone code for the country (e.g., "1" for United States).'),
            'currency': _('The primary currency used in this country.'),
            'is_active': _('Is this country currently active in the system?'),
        }
        error_messages = {
            'code': {
                'unique': _('A country with this code already exists.'),
            },
        }

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if code:
            code = code.upper()
            if len(code) != 2:
                raise forms.ValidationError(_('Country code must be exactly 2 characters long.'))
        return code

    def clean_phone_code(self):
        phone_code = self.cleaned_data.get('phone_code')
        if phone_code:
            if not phone_code.isdigit():
                raise forms.ValidationError(_('Phone code must contain only digits.'))
        return phone_code

# Translations for French
_ = lambda s: s
french_translations = {
    'Country Name': _('Nom du pays'),
    'Country Code': _('Code du pays'),
    'Phone Code': _('Indicatif téléphonique'),
    'Currency': _('Devise'),
    'Active': _('Actif'),
    'The full name of the country.': _('Le nom complet du pays.'),
    'The ISO 3166-1 alpha-2 country code (e.g., "US" for United States).': _('Le code pays ISO 3166-1 alpha-2 (par exemple, "FR" pour France).'),
    'The international phone code for the country (e.g., "1" for United States).': _("L'indicatif téléphonique international du pays (par exemple, '33' pour la France)."),
    'The primary currency used in this country.': _('La devise principale utilisée dans ce pays.'),
    'Is this country currently active in the system?': _('Ce pays est-il actuellement actif dans le système ?'),
    'A country with this code already exists.': _('Un pays avec ce code existe déjà.'),
    'Country code must be exactly 2 characters long.': _('Le code du pays doit comporter exactement 2 caractères.'),
    'Phone code must contain only digits.': _("L'indicatif téléphonique ne doit contenir que des chiffres."),
}

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['name', 'description', 'price', 'billing_cycle', 'features', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'billing_cycle': forms.Select(attrs={'class': 'form-control'}),
            'features': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': _('Plan Name'),
            'description': _('Description'),
            'price': _('Price'),
            'billing_cycle': _('Billing Cycle'),
            'features': _('Features'),
            'is_active': _('Active'),
        }
        help_texts = {
            'name': _('The name of the subscription plan.'),
            'description': _('A brief description of the plan.'),
            'price': _('The price of the plan.'),
            'billing_cycle': _('The billing cycle for this plan.'),
            'features': _('List of features included in this plan (one per line).'),
            'is_active': _('Is this plan currently active and available for purchase?'),
        }
        error_messages = {
            'name': {
                'unique': _('A plan with this name already exists.'),
            },
            'price': {
                'min_value': _('Price must be greater than or equal to 0.'),
            },
        }

    def clean_features(self):
        features = self.cleaned_data.get('features')
        if features:
            return [feature.strip() for feature in features.split('\n') if feature.strip()]
        return []

# Translations for French
_ = lambda s: s
french_translations = {
    'Plan Name': _('Nom du plan'),
    'Description': _('Description'),
    'Price': _('Prix'),
    'Billing Cycle': _('Cycle de facturation'),
    'Features': _('Fonctionnalités'),
    'Active': _('Actif'),
    'The name of the subscription plan.': _('Le nom du plan d\'abonnement.'),
    'A brief description of the plan.': _('Une brève description du plan.'),
    'The price of the plan.': _('Le prix du plan.'),
    'The billing cycle for this plan.': _('Le cycle de facturation pour ce plan.'),
    'List of features included in this plan (one per line).': _('Liste des fonctionnalités incluses dans ce plan (une par ligne).'),
    'Is this plan currently active and available for purchase?': _('Ce plan est-il actuellement actif et disponible à l\'achat ?'),
    'A plan with this name already exists.': _('Un plan avec ce nom existe déjà.'),
    'Price must be greater than or equal to 0.': _('Le prix doit être supérieur ou égal à 0.'),
}


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['name', 'description', 'version', 'is_core', 'dependencies', 'settings_schema', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'version': forms.TextInput(attrs={'class': 'form-control'}),
            'is_core': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dependencies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'settings_schema': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': _('Module Name'),
            'description': _('Description'),
            'version': _('Version'),
            'is_core': _('Core Module'),
            'dependencies': _('Dependencies'),
            'settings_schema': _('Settings Schema'),
            'is_active': _('Active'),
        }
        help_texts = {
            'name': _('The name of the module.'),
            'description': _('A brief description of the module.'),
            'version': _('The current version of the module.'),
            'is_core': _('Is this a core module of the system?'),
            'dependencies': _('List of other modules this module depends on (JSON format).'),
            'settings_schema': _('JSON schema for module settings.'),
            'is_active': _('Is this module currently active?'),
        }
        error_messages = {
            'name': {
                'unique': _('A module with this name already exists.'),
            },
        }

    def clean_dependencies(self):
        dependencies = self.cleaned_data.get('dependencies')
        if dependencies:
            try:
                import json
                json.loads(dependencies)
            except json.JSONDecodeError:
                raise forms.ValidationError(_('Invalid JSON format for dependencies.'))
        return dependencies

    def clean_settings_schema(self):
        settings_schema = self.cleaned_data.get('settings_schema')
        if settings_schema:
            try:
                import json
                json.loads(settings_schema)
            except json.JSONDecodeError:
                raise forms.ValidationError(_('Invalid JSON format for settings schema.'))
        return settings_schema

# Translations for French
_ = lambda s: s
french_translations.update({
    'Module Name': _('Nom du module'),
    'Description': _('Description'),
    'Version': _('Version'),
    'Core Module': _('Module principal'),
    'Dependencies': _('Dépendances'),
    'Settings Schema': _('Schéma des paramètres'),
    'Active': _('Actif'),
    'The name of the module.': _('Le nom du module.'),
    'A brief description of the module.': _('Une brève description du module.'),
    'The current version of the module.': _('La version actuelle du module.'),
    'Is this a core module of the system?': _('Est-ce un module principal du système ?'),
    'List of other modules this module depends on (JSON format).': _('Liste des autres modules dont ce module dépend (format JSON).'),
    'JSON schema for module settings.': _('Schéma JSON pour les paramètres du module.'),
    'Is this module currently active?': _('Ce module est-il actuellement actif ?'),
    'A module with this name already exists.': _('Un module avec ce nom existe déjà.'),
    'Invalid JSON format for dependencies.': _('Format JSON invalide pour les dépendances.'),
    'Invalid JSON format for settings schema.': _('Format JSON invalide pour le schéma des paramètres.'),
})



class AuditLogForm(forms.ModelForm):
    class Meta:
        model = AuditLog
        fields = ['user', 'action', 'entity_type', 'entity_id', 'changes', 'ip_address', 'user_agent']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'action': forms.TextInput(attrs={'class': 'form-control'}),
            'entity_type': forms.TextInput(attrs={'class': 'form-control'}),
            'entity_id': forms.TextInput(attrs={'class': 'form-control'}),
            'changes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ip_address': forms.TextInput(attrs={'class': 'form-control'}),
            'user_agent': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {
            'user': _('User'),
            'action': _('Action'),
            'entity_type': _('Entity Type'),
            'entity_id': _('Entity ID'),
            'changes': _('Changes'),
            'ip_address': _('IP Address'),
            'user_agent': _('User Agent'),
        }
        error_messages = {
            'user': {
                'required': _('Please select a user.'),
            },
            'action': {
                'required': _('Please enter an action.'),
                'max_length': _('The action must not exceed 50 characters.'),
            },
            'entity_type': {
                'required': _('Please enter an entity type.'),
                'max_length': _('The entity type must not exceed 100 characters.'),
            },
            'entity_id': {
                'required': _('Please enter an entity ID.'),
                'invalid': _('Please enter a valid UUID.'),
            },
            'ip_address': {
                'invalid': _('Please enter a valid IP address.'),
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].required = False  # Make user field optional

    def clean_changes(self):
        changes = self.cleaned_data.get('changes')
        if not isinstance(changes, dict):
            raise forms.ValidationError(_('Changes must be a valid JSON object.'))
        return changes

# French translations
_ = lambda s: s
french_translations = {
    'User': _('Utilisateur'),
    'Action': _('Action'),
    'Entity Type': _('Type d\'entité'),
    'Entity ID': _('ID d\'entité'),
    'Changes': _('Modifications'),
    'IP Address': _('Adresse IP'),
    'User Agent': _('Agent utilisateur'),
    'Please select a user.': _('Veuillez sélectionner un utilisateur.'),
    'Please enter an action.': _('Veuillez saisir une action.'),
    'The action must not exceed 50 characters.': _('L\'action ne doit pas dépasser 50 caractères.'),
    'Please enter an entity type.': _('Veuillez saisir un type d\'entité.'),
    'The entity type must not exceed 100 characters.': _('Le type d\'entité ne doit pas dépasser 100 caractères.'),
    'Please enter an entity ID.': _('Veuillez saisir un ID d\'entité.'),
    'Please enter a valid UUID.': _('Veuillez saisir un UUID valide.'),
    'Please enter a valid IP address.': _('Veuillez saisir une adresse IP valide.'),
    'Changes must be a valid JSON object.': _('Les modifications doivent être un objet JSON valide.'),
}

from django.utils.translation import gettext_lazy as _
from .models import Notification

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['recipient', 'type', 'title', 'message', 'data', 'read']
        widgets = {
            'recipient': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'data': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'read': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'recipient': _('Recipient'),
            'type': _('Type'),
            'title': _('Title'),
            'message': _('Message'),
            'data': _('Data'),
            'read': _('Read'),
        }
        error_messages = {
            'recipient': {
                'required': _('Please select a recipient.'),
            },
            'type': {
                'required': _('Please enter a notification type.'),
                'max_length': _('The type must not exceed 100 characters.'),
            },
            'title': {
                'required': _('Please enter a title.'),
                'max_length': _('The title must not exceed 200 characters.'),
            },
            'message': {
                'required': _('Please enter a message.'),
            },
        }

    def clean_data(self):
        data = self.cleaned_data.get('data')
        if not isinstance(data, dict):
            raise forms.ValidationError(_('Data must be a valid JSON object.'))
        return data

# French translations
_ = lambda s: s
french_translations = {
    'Recipient': _('Destinataire'),
    'Type': _('Type'),
    'Title': _('Titre'),
    'Message': _('Message'),
    'Data': _('Données'),
    'Read': _('Lu'),
    'Please select a recipient.': _('Veuillez sélectionner un destinataire.'),
    'Please enter a notification type.': _('Veuillez saisir un type de notification.'),
    'The type must not exceed 100 characters.': _('Le type ne doit pas dépasser 100 caractères.'),
    'Please enter a title.': _('Veuillez saisir un titre.'),
    'The title must not exceed 200 characters.': _('Le titre ne doit pas dépasser 200 caractères.'),
    'Please enter a message.': _('Veuillez saisir un message.'),
    'Data must be a valid JSON object.': _('Les données doivent être un objet JSON valide.'),
}