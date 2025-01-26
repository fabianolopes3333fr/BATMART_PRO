from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from companies.models import CompanyUser
from .models import MarketingCampaign, ContentManagement, EmailCampaign, MarketingAutomation, LeadManagement, MarketingMetrics
from django.forms.widgets import JSONInput

class MarketingCampaignForm(forms.ModelForm):
    class Meta:
        model = MarketingCampaign
        fields = ['company', 'content', 'name', 'description', 'campaign_type', 'status', 'start_date', 'end_date', 'budget', 'target_audience', 'goals', 'channels']
        
        labels = {
            'company': _('Company'),  # FR: Entreprise
            'content': _('Content'),  # FR: Contenu
            'name': _('Campaign Name'),  # FR: Nom de la campagne
            'description': _('Description'),  # FR: Description
            'campaign_type': _('Campaign Type'),  # FR: Type de campagne
            'status': _('Status'),  # FR: Statut
            'start_date': _('Start Date'),  # FR: Date de début
            'end_date': _('End Date'),  # FR: Date de fin
            'budget': _('Budget'),  # FR: Budget
            'target_audience': _('Target Audience'),  # FR: Public cible
            'goals': _('Goals'),  # FR: Objectifs
            'channels': _('Channels'),  # FR: Canaux
        }
        
        help_texts = {
            'campaign_type': _('Select the type of marketing campaign'),  # FR: Sélectionnez le type de campagne marketing
            'status': _('Select the current status of the campaign'),  # FR: Sélectionnez le statut actuel de la campagne
            'target_audience': _('Define the target audience for this campaign'),  # FR: Définissez le public cible pour cette campagne
            'goals': _('Set the goals for this campaign'),  # FR: Définissez les objectifs de cette campagne
            'channels': _('Select the channels for this campaign'),  # FR: Sélectionnez les canaux pour cette campagne
        }
        
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'target_audience': forms.JSONInput(),
            'goals': forms.JSONInput(),
            'channels': forms.JSONInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError(_("End date must be after start date."))  # FR: La date de fin doit être postérieure à la date de début.

        return cleaned_data

    def clean_budget(self):
        budget = self.cleaned_data.get('budget')
        if budget and budget <= 0:
            raise forms.ValidationError(_("Budget must be greater than zero."))  # FR: Le budget doit être supérieur à zéro.
        return budget

    content = forms.ModelMultipleChoiceField(
        queryset=ContentManagement.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label=_('Content'),  # FR: Contenu
        help_text=_('Select the content to be used in this campaign')  # FR: Sélectionnez le contenu à utiliser dans cette campagne
    )
    

class EmailCampaignForm(forms.ModelForm):
    class Meta:
        model = EmailCampaign
        fields = ['company', 'name', 'subject', 'content', 'sender_email', 'recipient_list', 'scheduled_time', 'status', 'email_template']
        
        labels = {
            'company': _('Company'),  # FR: Entreprise
            'name': _('Campaign Name'),  # FR: Nom de la campagne
            'subject': _('Email Subject'),  # FR: Objet de l'e-mail
            'content': _('Email Content'),  # FR: Contenu de l'e-mail
            'sender_email': _('Sender Email'),  # FR: E-mail de l'expéditeur
            'recipient_list': _('Recipient List'),  # FR: Liste des destinataires
            'scheduled_time': _('Scheduled Time'),  # FR: Heure programmée
            'status': _('Status'),  # FR: Statut
            'email_template': _('Email Template'),  # FR: Modèle d'e-mail
        }
        
        help_texts = {
            'subject': _('Enter the subject line for the email'),  # FR: Entrez l'objet de l'e-mail
            'content': _('Compose the main content of the email'),  # FR: Composez le contenu principal de l'e-mail
            'sender_email': _('Enter the email address that will appear as the sender'),  # FR: Entrez l'adresse e-mail qui apparaîtra comme expéditeur
            'recipient_list': _('Enter the list of recipient email addresses'),  # FR: Entrez la liste des adresses e-mail des destinataires
            'scheduled_time': _('Set the time for the email to be sent'),  # FR: Définissez l'heure d'envoi de l'e-mail
            'email_template': _('Select an email template to use'),  # FR: Sélectionnez un modèle d'e-mail à utiliser
        }
        
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
            'recipient_list': forms.Textarea(attrs={'rows': 5}),
            'scheduled_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_recipient_list(self):
        recipient_list = self.cleaned_data.get('recipient_list')
        if recipient_list:
            emails = [email.strip() for email in recipient_list.split(',')]
            for email in emails:
                if not forms.EmailField().clean(email):
                    raise forms.ValidationError(_("Invalid email address: %(email)s"), params={'email': email})
        return recipient_list

    def clean(self):
        cleaned_data = super().clean()
        scheduled_time = cleaned_data.get('scheduled_time')
        if scheduled_time and scheduled_time < timezone.now():
            raise forms.ValidationError(_("Scheduled time must be in the future."))  # FR: L'heure programmée doit être dans le futur.
        return cleaned_data

    email_template = forms.ModelChoiceField(
        queryset=ContentManagement.objects.filter(content_type='email_template'),
        required=False,
        label=_('Email Template'),  # FR: Modèle d'e-mail
        help_text=_('Select an email template to use for this campaign')  # FR: Sélectionnez un modèle d'e-mail à utiliser pour cette campagne
    )
    
class MarketingAutomationForm(forms.ModelForm):
    class Meta:
        model = MarketingAutomation
        fields = ['company', 'name', 'description', 'trigger_type', 'trigger_conditions', 'actions', 'is_active']
        
        labels = {
            'company': _('Company'),  # FR: Entreprise
            'name': _('Automation Name'),  # FR: Nom de l'automatisation
            'description': _('Description'),  # FR: Description
            'trigger_type': _('Trigger Type'),  # FR: Type de déclencheur
            'trigger_conditions': _('Trigger Conditions'),  # FR: Conditions de déclenchement
            'actions': _('Actions'),  # FR: Actions
            'is_active': _('Is Active'),  # FR: Est actif
        }
        
        help_texts = {
            'trigger_type': _('Select the type of trigger for this automation'),  # FR: Sélectionnez le type de déclencheur pour cette automatisation
            'trigger_conditions': _('Define the conditions that will trigger this automation'),  # FR: Définissez les conditions qui déclencheront cette automatisation
            'actions': _('Specify the actions to be performed when the trigger conditions are met'),  # FR: Spécifiez les actions à effectuer lorsque les conditions de déclenchement sont remplies
            'is_active': _('Check this box to activate the automation'),  # FR: Cochez cette case pour activer l'automatisation
        }
        
        widgets = {
            'trigger_conditions': forms.JSONInput(),
            'actions': forms.JSONInput(),
        }

    def clean_trigger_conditions(self):
        trigger_conditions = self.cleaned_data.get('trigger_conditions')
        if not trigger_conditions:
            raise forms.ValidationError(_("Trigger conditions are required."))  # FR: Les conditions de déclenchement sont requises.
        return trigger_conditions

    def clean_actions(self):
        actions = self.cleaned_data.get('actions')
        if not actions:
            raise forms.ValidationError(_("At least one action is required."))  # FR: Au moins une action est requise.
        return actions

    def clean(self):
        cleaned_data = super().clean()
        trigger_type = cleaned_data.get('trigger_type')
        trigger_conditions = cleaned_data.get('trigger_conditions')

        if trigger_type and trigger_conditions:
            if trigger_type == 'event' and 'event_name' not in trigger_conditions:
                raise forms.ValidationError(_("Event name is required for event-based triggers."))  # FR: Le nom de l'événement est requis pour les déclencheurs basés sur des événements.
            elif trigger_type == 'schedule' and 'schedule' not in trigger_conditions:
                raise forms.ValidationError(_("Schedule is required for time-based triggers."))  # FR: Un horaire est requis pour les déclencheurs basés sur le temps.

        return cleaned_data
    
    
class ContentManagementForm(forms.ModelForm):
    class Meta:
        model = ContentManagement
        fields = ['company', 'title', 'content_type', 'content', 'meta_description', 'keywords', 'author', 'publish_date', 'status', 'categories', 'tags', 'featured_image', 'seo_settings']
        
        labels = {
            'company': _('Company'),  # FR: Entreprise
            'title': _('Title'),  # FR: Titre
            'content_type': _('Content Type'),  # FR: Type de contenu
            'content': _('Content'),  # FR: Contenu
            'meta_description': _('Meta Description'),  # FR: Meta description
            'keywords': _('Keywords'),  # FR: Mots-clés
            'author': _('Author'),  # FR: Auteur
            'publish_date': _('Publish Date'),  # FR: Date de publication
            'status': _('Status'),  # FR: Statut
            'categories': _('Categories'),  # FR: Catégories
            'tags': _('Tags'),  # FR: Étiquettes
            'featured_image': _('Featured Image'),  # FR: Image à la une
            'seo_settings': _('SEO Settings'),  # FR: Paramètres SEO
        }
        
        help_texts = {
            'content_type': _('Select the type of content'),  # FR: Sélectionnez le type de contenu
            'meta_description': _('Enter a brief description for SEO purposes'),  # FR: Entrez une brève description à des fins de référencement
            'keywords': _('Enter keywords separated by commas'),  # FR: Entrez les mots-clés séparés par des virgules
            'publish_date': _('Set the date and time for publishing'),  # FR: Définissez la date et l'heure de publication
            'seo_settings': _('Enter additional SEO settings as JSON'),  # FR: Entrez des paramètres SEO supplémentaires au format JSON
        }
        
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
            'meta_description': forms.Textarea(attrs={'rows': 3}),
            'keywords': forms.TextInput(attrs={'placeholder': 'keyword1, keyword2, keyword3'}),
            'publish_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'categories': forms.JSONInput(),
            'tags': forms.JSONInput(),
            'featured_image': forms.JSONInput(),
            'seo_settings': forms.JSONInput(),
        }

    def clean_keywords(self):
        keywords = self.cleaned_data.get('keywords')
        if keywords:
            return [keyword.strip() for keyword in keywords.split(',')]
        return []

    def clean_publish_date(self):
        publish_date = self.cleaned_data.get('publish_date')
        if publish_date and publish_date < timezone.now():
            raise forms.ValidationError(_("Publish date cannot be in the past."))  # FR: La date de publication ne peut pas être dans le passé.
        return publish_date

    def clean_featured_image(self):
        featured_image = self.cleaned_data.get('featured_image')
        if featured_image and not isinstance(featured_image, dict):
            raise forms.ValidationError(_("Featured image must be a valid JSON object."))  # FR: L'image à la une doit être un objet JSON valide.
        return featured_image

    def clean_seo_settings(self):
        seo_settings = self.cleaned_data.get('seo_settings')
        if seo_settings and not isinstance(seo_settings, dict):
            raise forms.ValidationError(_("SEO settings must be a valid JSON object."))  # FR: Les paramètres SEO doivent être un objet JSON valide.
        return seo_settings
    
class LeadManagementForm(forms.ModelForm):
    class Meta:
        model = LeadManagement
        fields = ['company', 'name', 'email', 'phone', 'source', 'status', 'notes', 'assigned_to', 'last_contact_date']
        
        labels = {
            'company': _('Company'),  # FR: Entreprise
            'name': _('Name'),  # FR: Nom
            'email': _('Email'),  # FR: E-mail
            'phone': _('Phone'),  # FR: Téléphone
            'source': _('Source'),  # FR: Source
            'status': _('Status'),  # FR: Statut
            'notes': _('Notes'),  # FR: Notes
            'assigned_to': _('Assigned To'),  # FR: Assigné à
            'last_contact_date': _('Last Contact Date'),  # FR: Date du dernier contact
        }
        
        help_texts = {
            'source': _('Where did this lead come from?'),  # FR: D'où vient ce lead ?
            'status': _('Current status of the lead'),  # FR: Statut actuel du lead
            'assigned_to': _('Team member responsible for this lead'),  # FR: Membre de l'équipe responsable de ce lead
        }
        
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
            'last_contact_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not forms.EmailField().clean(email):
            raise forms.ValidationError(_("Invalid email address."))  # FR: Adresse e-mail invalide.
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove non-digit characters
            phone = ''.join(filter(str.isdigit, phone))
            if len(phone) < 10:
                raise forms.ValidationError(_("Phone number must have at least 10 digits."))  # FR: Le numéro de téléphone doit avoir au moins 10 chiffres.
        return phone

    def clean(self):
        cleaned_data = super().clean()
        last_contact_date = cleaned_data.get('last_contact_date')
        if last_contact_date and last_contact_date > timezone.now():
            raise forms.ValidationError(_("Last contact date cannot be in the future."))  # FR: La date du dernier contact ne peut pas être dans le futur.
        return cleaned_data

    assigned_to = forms.ModelChoiceField(
        queryset=CompanyUser.objects.all(),
        required=False,
        label=_('Assigned To'),  # FR: Assigné à
        help_text=_('Select the team member responsible for this lead')  # FR: Sélectionnez le membre de l'équipe responsable de ce lead
    )
    
class MarketingMetricsForm(forms.ModelForm):
    class Meta:
        model = MarketingMetrics
        fields = ['company', 'campaign', 'metric_type', 'value', 'date', 'source']
        
        labels = {
            'company': _('Company'),  # FR: Entreprise
            'campaign': _('Campaign'),  # FR: Campagne
            'metric_type': _('Metric Type'),  # FR: Type de métrique
            'value': _('Value'),  # FR: Valeur
            'date': _('Date'),  # FR: Date
            'source': _('Source'),  # FR: Source
        }
        
        help_texts = {
            'metric_type': _('Select the type of marketing metric'),  # FR: Sélectionnez le type de métrique marketing
            'value': _('Enter the numeric value for this metric'),  # FR: Entrez la valeur numérique pour cette métrique
            'source': _('Specify the source of this metric data'),  # FR: Spécifiez la source de ces données métriques
        }
        
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_value(self):
        value = self.cleaned_data.get('value')
        if value is not None and value < 0:
            raise forms.ValidationError(_("Value must be non-negative."))  # FR: La valeur doit être non négative.
        return value

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        if date and date > timezone.now():
            raise forms.ValidationError(_("Date cannot be in the future."))  # FR: La date ne peut pas être dans le futur.
        return cleaned_data

    campaign = forms.ModelChoiceField(
        queryset=MarketingCampaign.objects.all(),
        required=False,
        label=_('Campaign'),  # FR: Campagne
        help_text=_('Select the associated marketing campaign (if applicable)')  # FR: Sélectionnez la campagne marketing associée (si applicable)
    )