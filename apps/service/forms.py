from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import Service, ServiceAppointment, ServiceQuote, ServiceDeliverable, ServiceReview
from django.forms.widgets import JSONInput

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['company', 'name', 'description', 'base_price', 'duration_minutes', 'pricing_model', 
                  'availability_rules', 'booking_settings', 'requires_quote', 'qualification_required', 
                  'is_active', 'categories']
        
        labels = {
            'company': _('Company'),  # FR: Entreprise
            'name': _('Service Name'),  # FR: Nom du service
            'description': _('Description'),  # FR: Description
            'base_price': _('Base Price'),  # FR: Prix de base
            'duration_minutes': _('Duration (minutes)'),  # FR: Durée (minutes)
            'pricing_model': _('Pricing Model'),  # FR: Modèle de tarification
            'availability_rules': _('Availability Rules'),  # FR: Règles de disponibilité
            'booking_settings': _('Booking Settings'),  # FR: Paramètres de réservation
            'requires_quote': _('Requires Quote'),  # FR: Nécessite un devis
            'qualification_required': _('Qualification Required'),  # FR: Qualification requise
            'is_active': _('Is Active'),  # FR: Est actif
            'categories': _('Categories'),  # FR: Catégories
        }
        
        help_texts = {
            'base_price': _('The base price for this service.'),  # FR: Le prix de base pour ce service.
            'duration_minutes': _('The expected duration of the service in minutes.'),  # FR: La durée prévue du service en minutes.
            'requires_quote': _('Check if this service requires a quote before booking.'),  # FR: Cochez si ce service nécessite un devis avant la réservation.
            'is_active': _('Uncheck to temporarily disable this service.'),  # FR: Décochez pour désactiver temporairement ce service.
        }
        
        error_messages = {
            'base_price': {
                'invalid': _('Please enter a valid price.'),  # FR: Veuillez entrer un prix valide.
            },
            'duration_minutes': {
                'invalid': _('Please enter a valid duration in minutes.'),  # FR: Veuillez entrer une durée valide en minutes.
            },
        }
        
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'pricing_model': forms.JSONInput(),
            'availability_rules': forms.JSONInput(),
            'booking_settings': forms.JSONInput(),
            'qualification_required': forms.JSONInput(),
            'categories': forms.JSONInput(),
        }

    def clean_duration_minutes(self):
        duration = self.cleaned_data.get('duration_minutes')
        if duration is not None and duration <= 0:
            raise forms.ValidationError(_("Duration must be a positive number."))  # FR: La durée doit être un nombre positif.
        return duration

    def clean_base_price(self):
        price = self.cleaned_data.get('base_price')
        if price is not None and price < 0:
            raise forms.ValidationError(_("Base price cannot be negative."))  # FR: Le prix de base ne peut pas être négatif.
        return price
    
    

class ServiceAppointmentForm(forms.ModelForm):
    class Meta:
        model = ServiceAppointment
        fields = ['service', 'customer', 'scheduled_start', 'scheduled_end', 'status']
        
        labels = {
            'service': _('Service'),  # FR: Service
            'customer': _('Customer'),  # FR: Client
            'scheduled_start': _('Scheduled Start'),  # FR: Début prévu
            'scheduled_end': _('Scheduled End'),  # FR: Fin prévue
            'status': _('Status'),  # FR: Statut
        }
        
        help_texts = {
            'scheduled_start': _('The start time of the appointment.'),  # FR: L'heure de début du rendez-vous.
            'scheduled_end': _('The end time of the appointment.'),  # FR: L'heure de fin du rendez-vous.
            'status': _('Current status of the appointment.'),  # FR: Statut actuel du rendez-vous.
        }
        
        error_messages = {
            'scheduled_start': {
                'invalid': _('Please enter a valid start time.'),  # FR: Veuillez entrer une heure de début valide.
            },
            'scheduled_end': {
                'invalid': _('Please enter a valid end time.'),  # FR: Veuillez entrer une heure de fin valide.
            },
        }
        
        widgets = {
            'scheduled_start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'scheduled_end': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'status': forms.Select(choices=ServiceAppointment.STATUS_CHOICES),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("scheduled_start")
        end = cleaned_data.get("scheduled_end")

        if start and end:
            if start >= end:
                raise forms.ValidationError(_("End time must be after start time."))  # FR: L'heure de fin doit être après l'heure de début.

        return cleaned_data

    def clean_status(self):
        status = self.cleaned_data.get('status')
        if status not in dict(ServiceAppointment.STATUS_CHOICES):
            raise forms.ValidationError(_("Invalid status selected."))  # FR: Statut sélectionné invalide.
        return status
    
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Service, ServiceAppointment, ServiceQuote
from django.forms.widgets import JSONInput

# ... (código existente) ...

class ServiceQuoteForm(forms.ModelForm):
    class Meta:
        model = ServiceQuote
        fields = ['service', 'customer', 'requirements', 'specifications', 'estimated_duration', 
                  'estimated_cost', 'valid_until', 'status', 'notes', 'terms_conditions']
        
        labels = {
            'service': _('Service'),  # FR: Service
            'customer': _('Customer'),  # FR: Client
            'requirements': _('Requirements'),  # FR: Exigences
            'specifications': _('Specifications'),  # FR: Spécifications
            'estimated_duration': _('Estimated Duration (minutes)'),  # FR: Durée estimée (minutes)
            'estimated_cost': _('Estimated Cost'),  # FR: Coût estimé
            'valid_until': _('Valid Until'),  # FR: Valable jusqu'au
            'status': _('Status'),  # FR: Statut
            'notes': _('Notes'),  # FR: Notes
            'terms_conditions': _('Terms and Conditions'),  # FR: Termes et conditions
        }
        
        help_texts = {
            'estimated_duration': _('Estimated duration of the service in minutes.'),  # FR: Durée estimée du service en minutes.
            'estimated_cost': _('Estimated cost of the service.'),  # FR: Coût estimé du service.
            'valid_until': _('The date until which this quote is valid.'),  # FR: La date jusqu'à laquelle ce devis est valable.
        }
        
        error_messages = {
            'estimated_duration': {
                'invalid': _('Please enter a valid duration in minutes.'),  # FR: Veuillez entrer une durée valide en minutes.
            },
            'estimated_cost': {
                'invalid': _('Please enter a valid cost.'),  # FR: Veuillez entrer un coût valide.
            },
            'valid_until': {
                'invalid': _('Please enter a valid date.'),  # FR: Veuillez entrer une date valide.
            },
        }
        
        widgets = {
            'requirements': forms.Textarea(attrs={'rows': 3}),
            'specifications': JSONInput(),
            'valid_until': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'status': forms.Select(choices=ServiceQuote.STATUS_CHOICES),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'terms_conditions': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_estimated_duration(self):
        duration = self.cleaned_data.get('estimated_duration')
        if duration is not None and duration <= 0:
            raise forms.ValidationError(_("Estimated duration must be a positive number."))  # FR: La durée estimée doit être un nombre positif.
        return duration

    def clean_estimated_cost(self):
        cost = self.cleaned_data.get('estimated_cost')
        if cost is not None and cost < 0:
            raise forms.ValidationError(_("Estimated cost cannot be negative."))  # FR: Le coût estimé ne peut pas être négatif.
        return cost

    def clean_valid_until(self):
        valid_until = self.cleaned_data.get('valid_until')
        if valid_until and valid_until < timezone.now():
            raise forms.ValidationError(_("Valid until date must be in the future."))  # FR: La date de validité doit être dans le futur.
        return valid_until

    def clean_status(self):
        status = self.cleaned_data.get('status')
        if status not in dict(ServiceQuote.STATUS_CHOICES):
            raise forms.ValidationError(_("Invalid status selected."))  # FR: Statut sélectionné invalide.
        return status
    
    

class ServiceDeliverableForm(forms.ModelForm):
    class Meta:
        model = ServiceDeliverable
        fields = ['appointment', 'name', 'description', 'status', 'due_date', 'completed_date', 
                  'attachments', 'verification_required', 'verification_status']
        
        labels = {
            'appointment': _('Appointment'),  # FR: Rendez-vous
            'name': _('Deliverable Name'),  # FR: Nom du livrable
            'description': _('Description'),  # FR: Description
            'status': _('Status'),  # FR: Statut
            'due_date': _('Due Date'),  # FR: Date d'échéance
            'completed_date': _('Completed Date'),  # FR: Date de réalisation
            'attachments': _('Attachments'),  # FR: Pièces jointes
            'verification_required': _('Verification Required'),  # FR: Vérification requise
            'verification_status': _('Verification Status'),  # FR: Statut de vérification
        }
        
        help_texts = {
            'due_date': _('The date by which this deliverable is due.'),  # FR: La date à laquelle ce livrable est dû.
            'completed_date': _('The date when this deliverable was completed.'),  # FR: La date à laquelle ce livrable a été terminé.
            'verification_required': _('Check if this deliverable requires verification.'),  # FR: Cochez si ce livrable nécessite une vérification.
        }
        
        error_messages = {
            'due_date': {
                'invalid': _('Please enter a valid due date.'),  # FR: Veuillez entrer une date d'échéance valide.
            },
            'completed_date': {
                'invalid': _('Please enter a valid completion date.'),  # FR: Veuillez entrer une date de réalisation valide.
            },
        }
        
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'status': forms.Select(choices=ServiceDeliverable.STATUS_CHOICES),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'completed_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'attachments': JSONInput(),
            'verification_status': JSONInput(),
        }

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < timezone.now():
            raise forms.ValidationError(_("Due date must be in the future."))  # FR: La date d'échéance doit être dans le futur.
        return due_date

    def clean_completed_date(self):
        completed_date = self.cleaned_data.get('completed_date')
        due_date = self.cleaned_data.get('due_date')
        if completed_date and due_date and completed_date > due_date:
            raise forms.ValidationError(_("Completed date cannot be after the due date."))  # FR: La date de réalisation ne peut pas être après la date d'échéance.
        return completed_date

    def clean_status(self):
        status = self.cleaned_data.get('status')
        if status not in dict(ServiceDeliverable.STATUS_CHOICES):
            raise forms.ValidationError(_("Invalid status selected."))  # FR: Statut sélectionné invalide.
        return status
    


class ServiceReviewForm(forms.ModelForm):
    class Meta:
        model = ServiceReview
        fields = ['appointment', 'customer', 'rating', 'review_text', 'attributes', 'is_public']
        
        labels = {
            'appointment': _('Appointment'),  # FR: Rendez-vous
            'customer': _('Customer'),  # FR: Client
            'rating': _('Rating'),  # FR: Évaluation
            'review_text': _('Review Text'),  # FR: Texte de l'avis
            'attributes': _('Attributes'),  # FR: Attributs
            'is_public': _('Is Public'),  # FR: Est public
        }
        
        help_texts = {
            'rating': _('Rate the service from 1 to 5.'),  # FR: Évaluez le service de 1 à 5.
            'attributes': _('Additional attributes like punctuality, quality, etc.'),  # FR: Attributs supplémentaires comme la ponctualité, la qualité, etc.
            'is_public': _('Check if this review should be publicly visible.'),  # FR: Cochez si cet avis doit être visible publiquement.
        }
        
        error_messages = {
            'rating': {
                'invalid': _('Please enter a valid rating between 1 and 5.'),  # FR: Veuillez entrer une évaluation valide entre 1 et 5.
            },
        }
        
        widgets = {
            'review_text': forms.Textarea(attrs={'rows': 3}),
            'attributes': JSONInput(),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is not None and (rating < 1 or rating > 5):
            raise forms.ValidationError(_("Rating must be between 1 and 5."))  # FR: L'évaluation doit être comprise entre 1 et 5.
        return rating

    def clean_attributes(self):
        attributes = self.cleaned_data.get('attributes')
        if not isinstance(attributes, dict):
            raise forms.ValidationError(_("Attributes must be a valid JSON object."))  # FR: Les attributs doivent être un objet JSON valide.
        return attributes