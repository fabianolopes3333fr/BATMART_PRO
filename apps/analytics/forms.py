from django import forms
from django.utils.translation import gettext_lazy as _
from .models import ReportExecution, Report, Dashboard, Metric, Alert, DataExport

# Traduções em francês
_('Template must be a valid JSON object.') # Tradução: "Le modèle doit être un objet JSON valide."
_('Parameters must be a valid JSON object.') # Tradução: "Les paramètres doivent être un objet JSON valide."
_('Schedule must be a valid JSON object.') # Tradução: "Le planning doit être un objet JSON valide."
_('Recipients must be a valid JSON array.') # Tradução: "Les destinataires doivent être un tableau JSON valide."
_('Custom reports must include a custom query in the template.') # Tradução: "Les rapports personnalisés doivent inclure une requête personnalisée dans le modèle."
_('Parameters used must be a valid JSON object.') # Tradução: "Les paramètres utilisés doivent être un objet JSON valide."
_('Result data must be a valid JSON object.') # Tradução: "Les données de résultat doivent être un objet JSON valide."
_('File output must be a valid JSON object.') # Tradução: "La sortie de fichier doit être un objet JSON valide."
_('End time cannot be before start time.') # Tradução: "L'heure de fin ne peut pas être antérieure à l'heure de début."
_('End time is required for completed executions.') # Tradução: "L'heure de fin est requise pour les exécutions terminées."
_('Error message is required for failed executions.') # Tradução: "Un message d'erreur est requis pour les exécutions échouées."
_("La configuration de mise en page doit être un objet JSON valide.") # Tradução: "The layout configuration must be a valid JSON object."
_("La liste des widgets doit être un tableau JSON valide.") # Tradução: "The widget list must be a valid JSON array."
_("Les permissions doivent être un objet JSON valide.") # Tradução: "The permissions must be a valid JSON object."

# French translations
# _("Calculation must be a valid JSON object.") -> "Le calcul doit être un objet JSON valide."
# _("Dimensions must be a valid JSON array.") -> "Les dimensions doivent être un tableau JSON valide."
# _("Filters must be a valid JSON object.") -> "Les filtres doivent être un objet JSON valide."

# Add these translations to your translation files
_("Calculation must be a valid JSON object.")
_("Dimensions must be a valid JSON array.")
_("Filters must be a valid JSON object.")

# French translations
# _("Threshold value is required.") -> "La valeur seuil est requise."
# _("Recipients must be a valid JSON array.") -> "Les destinataires doivent être un tableau JSON valide."
# _("Threshold for percentage metrics must be between 0 and 100.") -> "Le seuil pour les métriques en pourcentage doit être compris entre 0 et 100."

# Add these translations to your translation files
_("Threshold value is required.")
_("Recipients must be a valid JSON array.")
_("Threshold for percentage metrics must be between 0 and 100.")

# French translations
# _("Filters must be a valid JSON object.") -> "Les filtres doivent être un objet JSON valide."
# _("Columns must be a valid JSON array.") -> "Les colonnes doivent être un tableau JSON valide."
# _("Schedule must be a valid JSON object.") -> "Le calendrier doit être un objet JSON valide."
# _("Recipients must be a valid JSON array.") -> "Les destinataires doivent être un tableau JSON valide."
# _("Schedule is required for scheduled exports.") -> "Un calendrier est requis pour les exportations programmées."
# _("Data source is required for API exports.") -> "Une source de données est requise pour les exportations API."

# Add these translations to your translation files
_("Filters must be a valid JSON object.")
_("Columns must be a valid JSON array.")
_("Schedule must be a valid JSON object.")
_("Recipients must be a valid JSON array.")
_("Schedule is required for scheduled exports.")
_("Data source is required for API exports.")

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['company', 'name', 'description', 'report_type', 'template', 'parameters', 'schedule', 'recipients', 'created_by']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'template': forms.JSONField(),
            'parameters': forms.JSONField(),
            'schedule': forms.JSONField(),
            'recipients': forms.JSONField(),
        }


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user and self.user.company:
            self.fields['company'].initial = self.user.company
            self.fields['company'].widget = forms.HiddenInput()
            self.fields['created_by'].initial = self.user
            self.fields['created_by'].widget = forms.HiddenInput()

    def clean_template(self):
        template = self.cleaned_data.get('template')
        if not isinstance(template, dict):
            raise forms.ValidationError(_("Template must be a valid JSON object."))
        return template

    def clean_parameters(self):
        parameters = self.cleaned_data.get('parameters')
        if not isinstance(parameters, dict):
            raise forms.ValidationError(_("Parameters must be a valid JSON object."))
        return parameters

    def clean_schedule(self):
        schedule = self.cleaned_data.get('schedule')
        if not isinstance(schedule, dict):
            raise forms.ValidationError(_("Schedule must be a valid JSON object."))
        return schedule

    def clean_recipients(self):
        recipients = self.cleaned_data.get('recipients')
        if not isinstance(recipients, list):
            raise forms.ValidationError(_("Recipients must be a valid JSON array."))
        return recipients

    def clean(self):
        cleaned_data = super().clean()
        report_type = cleaned_data.get('report_type')
        template = cleaned_data.get('template')

        if report_type and template:
            if report_type == 'custom' and not template.get('custom_query'):
                raise forms.ValidationError(_("Custom reports must include a custom query in the template."))
        
        return cleaned_data
class ReportExecutionForm(forms.ModelForm):
    class Meta:
        model = ReportExecution
        fields = ['report', 'executed_by', 'start_time', 'end_time', 'status', 'parameters_used', 'result_data', 'error_message', 'file_output']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'parameters_used': forms.JSONField(),
            'result_data': forms.JSONField(),
            'file_output': forms.JSONField(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            if 'executed_by' in self.fields:
                self.fields['executed_by'].initial = self.user
                self.fields['executed_by'].widget = forms.HiddenInput()
            
            # Limitar as opções de relatório aos relatórios da empresa do usuário
            if self.user.company and 'report' in self.fields:
                report_field = self.fields['report']
                if isinstance(report_field, forms.ModelChoiceField):
                    report_field.queryset = Report.objects.filter(company=self.user.company)

    def clean_parameters_used(self):
        parameters_used = self.cleaned_data.get('parameters_used')
        if not isinstance(parameters_used, dict):
            raise forms.ValidationError(_("Parameters used must be a valid JSON object."))
        return parameters_used

    def clean_result_data(self):
        result_data = self.cleaned_data.get('result_data')
        if result_data and not isinstance(result_data, dict):
            raise forms.ValidationError(_("Result data must be a valid JSON object."))
        return result_data

    def clean_file_output(self):
        file_output = self.cleaned_data.get('file_output')
        if not isinstance(file_output, dict):
            raise forms.ValidationError(_("File output must be a valid JSON object."))
        return file_output

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        status = cleaned_data.get('status')

        if end_time and start_time and end_time < start_time:
            raise forms.ValidationError(_("End time cannot be before start time."))

        if status == 'completed' and not end_time:
            raise forms.ValidationError(_("End time is required for completed executions."))

        if status == 'failed' and not cleaned_data.get('error_message'):
            raise forms.ValidationError(_("Error message is required for failed executions."))

        return cleaned_data
    
class DashboardForm(forms.ModelForm):
    class Meta:
        model = Dashboard
        fields = ['company', 'name', 'description', 'layout', 'widgets', 'permissions', 'is_default', 'created_by']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'layout': forms.JSONField(),
            'widgets': forms.JSONField(),
            'permissions': forms.JSONField(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user and self.user.company:
            self.fields['company'].initial = self.user.company
            self.fields['company'].widget = forms.HiddenInput()
            self.fields['created_by'].initial = self.user
            self.fields['created_by'].widget = forms.HiddenInput()

    def clean_layout(self):
        layout = self.cleaned_data.get('layout')
        if not isinstance(layout, dict):
            raise forms.ValidationError(_("La configuration de mise en page doit être un objet JSON valide."))
        return layout

    def clean_widgets(self):
        widgets = self.cleaned_data.get('widgets')
        if not isinstance(widgets, list):
            raise forms.ValidationError(_("La liste des widgets doit être un tableau JSON valide."))
        return widgets

    def clean_permissions(self):
        permissions = self.cleaned_data.get('permissions')
        if not isinstance(permissions, dict):
            raise forms.ValidationError(_("Les permissions doivent être un objet JSON valide."))
        return permissions
    
    
class MetricForm(forms.ModelForm):
    class Meta:
        model = Metric
        fields = ['company', 'name', 'description', 'metric_type', 'calculation', 'dimensions', 'filters', 'update_frequency', 'alerts', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'calculation': forms.JSONField(),
            'dimensions': forms.JSONField(),
            'filters': forms.JSONField(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user and self.user.company:
            self.fields['company'].initial = self.user.company
            self.fields['company'].widget = forms.HiddenInput()

    def clean_calculation(self):
        calculation = self.cleaned_data.get('calculation')
        if not isinstance(calculation, dict):
            raise forms.ValidationError(_("Calculation must be a valid JSON object."))
        return calculation

    def clean_dimensions(self):
        dimensions = self.cleaned_data.get('dimensions')
        if not isinstance(dimensions, list):
            raise forms.ValidationError(_("Dimensions must be a valid JSON array."))
        return dimensions

    def clean_filters(self):
        filters = self.cleaned_data.get('filters')
        if not isinstance(filters, dict):
            raise forms.ValidationError(_("Filters must be a valid JSON object."))
        return filters

class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = ['company', 'name', 'description', 'metric', 'condition', 'threshold', 'frequency', 'recipients', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'condition': forms.Select(choices=Alert.CONDITION_CHOICES),
            'recipients': forms.JSONField(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user and hasattr(self.user, 'company') and self.user.company:
            if 'company' in self.fields:
                self.fields['company'].initial = self.user.company
                self.fields['company'].widget = forms.HiddenInput()
            
            if 'metric' in self.fields:
                metric_field = self.fields['metric']
                if isinstance(metric_field, forms.ModelChoiceField):
                    metric_field.queryset = Metric.objects.filter(company=self.user.company)
        elif self.user and not getattr(self.user, 'company', None):
            # Desabilitar campos relacionados à empresa
            for field_name in ['company', 'metric']:
                if field_name in self.fields:
                    self.fields[field_name].disabled = True
            # Adicionar uma mensagem de erro ou aviso
            self.add_error(None, _("User does not have an associated company. Some features may be limited."))
        else:
            # Caso o usuário não esteja autenticado ou haja outro problema
            self.add_error(None, _("Invalid user data. Please log in again."))


    def clean_threshold(self):
        threshold = self.cleaned_data.get('threshold')
        if threshold is None:
            raise forms.ValidationError(_("Threshold value is required."))
        return threshold

    def clean_recipients(self):
        recipients = self.cleaned_data.get('recipients')
        if not isinstance(recipients, list):
            raise forms.ValidationError(_("Recipients must be a valid JSON array."))
        return recipients

    def clean(self):
        cleaned_data = super().clean()
        condition = cleaned_data.get('condition')
        threshold = cleaned_data.get('threshold')
        
        if condition and threshold is not None:
            metric = cleaned_data.get('metric')
            if metric and metric.metric_type == 'percentage' and (threshold < 0 or threshold > 100):
                self.add_error('threshold', _("Threshold for percentage metrics must be between 0 and 100."))

        return cleaned_data
    
class DataExportForm(forms.ModelForm):
    class Meta:
        model = DataExport
        fields = ['company', 'name', 'description', 'export_type', 'data_source', 'filters', 'columns', 'format', 'schedule', 'recipients', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'filters': forms.JSONField(),
            'columns': forms.JSONField(),
            'schedule': forms.JSONField(),
            'recipients': forms.JSONField(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user and self.user.company:
            self.fields['company'].initial = self.user.company
            self.fields['company'].widget = forms.HiddenInput()

    def clean_filters(self):
        filters = self.cleaned_data.get('filters')
        if not isinstance(filters, dict):
            raise forms.ValidationError(_("Filters must be a valid JSON object."))
        return filters

    def clean_columns(self):
        columns = self.cleaned_data.get('columns')
        if not isinstance(columns, list):
            raise forms.ValidationError(_("Columns must be a valid JSON array."))
        return columns

    def clean_schedule(self):
        schedule = self.cleaned_data.get('schedule')
        if not isinstance(schedule, dict):
            raise forms.ValidationError(_("Schedule must be a valid JSON object."))
        return schedule

    def clean_recipients(self):
        recipients = self.cleaned_data.get('recipients')
        if not isinstance(recipients, list):
            raise forms.ValidationError(_("Recipients must be a valid JSON array."))
        return recipients

    def clean(self):
        cleaned_data = super().clean()
        export_type = cleaned_data.get('export_type')
        data_source = cleaned_data.get('data_source')

        if export_type == 'scheduled' and not cleaned_data.get('schedule'):
            self.add_error('schedule', _("Schedule is required for scheduled exports."))

        if export_type == 'api' and not data_source:
            self.add_error('data_source', _("Data source is required for API exports."))

        return cleaned_data