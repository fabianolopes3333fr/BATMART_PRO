from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import Project, ProjectMember, ProjectPhase, ProjectTask, ProjectResource, ProjectIssue, ProjectTimeEntry
from django.forms.widgets import JSONInput

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['company', 'customer', 'name', 'description', 'start_date', 'end_date', 'status', 'priority', 'budget', 'actual_cost', 'team_members', 'documents', 'custom_fields']
        
        labels = {
            'company': _('Company'),  # FR: Entreprise
            'customer': _('Customer'),  # FR: Client
            'name': _('Project Name'),  # FR: Nom du projet
            'description': _('Description'),  # FR: Description
            'start_date': _('Start Date'),  # FR: Date de début
            'end_date': _('End Date'),  # FR: Date de fin
            'status': _('Status'),  # FR: Statut
            'priority': _('Priority'),  # FR: Priorité
            'budget': _('Budget'),  # FR: Budget
            'actual_cost': _('Actual Cost'),  # FR: Coût réel
            'team_members': _('Team Members'),  # FR: Membres de l'équipe
            'documents': _('Documents'),  # FR: Documents
            'custom_fields': _('Custom Fields'),  # FR: Champs personnalisés
        }
        
        help_texts = {
            'start_date': _('The date when the project starts.'),  # FR: La date de début du projet.
            'end_date': _('The date when the project is expected to end.'),  # FR: La date prévue de fin du projet.
            'budget': _('The total budget allocated for the project.'),  # FR: Le budget total alloué au projet.
            'actual_cost': _('The current actual cost of the project.'),  # FR: Le coût réel actuel du projet.
        }
        
        error_messages = {
            'end_date': {
                'invalid': _('End date must be after start date.'),  # FR: La date de fin doit être postérieure à la date de début.
            },
        }
        
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'documents': forms.JSONInput(),
            'custom_fields': forms.JSONInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date <= start_date:
            raise forms.ValidationError(_("End date must be after start date."))  # FR: La date de fin doit être postérieure à la date de début.

        return cleaned_data
    


class ProjectMemberForm(forms.ModelForm):
    class Meta:
        model = ProjectMember
        fields = ['project', 'user', 'role', 'responsibilities', 'allocation_percentage', 'start_date', 'end_date', 'hourly_rate']
        
        labels = {
            'project': _('Project'),  # FR: Projet
            'user': _('User'),  # FR: Utilisateur
            'role': _('Role'),  # FR: Rôle
            'responsibilities': _('Responsibilities'),  # FR: Responsabilités
            'allocation_percentage': _('Allocation Percentage'),  # FR: Pourcentage d'allocation
            'start_date': _('Start Date'),  # FR: Date de début
            'end_date': _('End Date'),  # FR: Date de fin
            'hourly_rate': _('Hourly Rate'),  # FR: Taux horaire
        }
        
        help_texts = {
            'allocation_percentage': _('Percentage of time allocated to this project.'),  # FR: Pourcentage de temps alloué à ce projet.
            'start_date': _('The date when the member starts working on the project.'),  # FR: La date à laquelle le membre commence à travailler sur le projet.
            'end_date': _('The date when the member is expected to finish working on the project.'),  # FR: La date à laquelle le membre devrait terminer son travail sur le projet.
            'hourly_rate': _('The hourly rate for this team member (if applicable).'),  # FR: Le taux horaire pour ce membre de l'équipe (si applicable).
        }
        
        error_messages = {
            'allocation_percentage': {
                'invalid': _('Allocation percentage must be between 0 and 100.'),  # FR: Le pourcentage d'allocation doit être compris entre 0 et 100.
            },
            'end_date': {
                'invalid': _('End date must be after start date.'),  # FR: La date de fin doit être postérieure à la date de début.
            },
        }
        
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'responsibilities': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        allocation_percentage = cleaned_data.get('allocation_percentage')

        if start_date and end_date and end_date <= start_date:
            raise forms.ValidationError(_("End date must be after start date."))  # FR: La date de fin doit être postérieure à la date de début.

        if allocation_percentage is not None and (allocation_percentage < 0 or allocation_percentage > 100):
            raise forms.ValidationError(_("Allocation percentage must be between 0 and 100."))  # FR: Le pourcentage d'allocation doit être compris entre 0 et 100.

        return cleaned_data

    
class ProjectPhaseForm(forms.ModelForm):
    class Meta:
        model = ProjectPhase
        fields = ['project', 'name', 'description', 'start_date', 'end_date', 'status', 'deliverables', 'milestones']
        
        labels = {
            'project': _('Project'),  # FR: Projet
            'name': _('Phase Name'),  # FR: Nom de la phase
            'description': _('Description'),  # FR: Description
            'start_date': _('Start Date'),  # FR: Date de début
            'end_date': _('End Date'),  # FR: Date de fin
            'status': _('Status'),  # FR: Statut
            'deliverables': _('Deliverables'),  # FR: Livrables
            'milestones': _('Milestones'),  # FR: Jalons
        }
        
        help_texts = {
            'start_date': _('The date when the phase starts.'),  # FR: La date de début de la phase.
            'end_date': _('The date when the phase is expected to end.'),  # FR: La date prévue de fin de la phase.
            'deliverables': _('List of deliverables for this phase.'),  # FR: Liste des livrables pour cette phase.
            'milestones': _('Key milestones for this phase.'),  # FR: Jalons clés pour cette phase.
        }
        
        error_messages = {
            'end_date': {
                'invalid': _('End date must be after start date.'),  # FR: La date de fin doit être postérieure à la date de début.
            },
        }
        
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'deliverables': forms.JSONInput(),
            'milestones': forms.JSONInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date <= start_date:
            raise forms.ValidationError(_("End date must be after start date."))  # FR: La date de fin doit être postérieure à la date de début.

        return cleaned_data
    
class ProjectTaskForm(forms.ModelForm):
    class Meta:
        model = ProjectTask
        fields = ['project', 'phase', 'name', 'description', 'assigned_to', 'start_date', 'end_date', 'status', 'priority', 'estimated_hours', 'actual_hours', 'dependencies', 'attachments']
        
        labels = {
            'project': _('Project'),  # FR: Projet
            'phase': _('Phase'),  # FR: Phase
            'name': _('Task Name'),  # FR: Nom de la tâche
            'description': _('Description'),  # FR: Description
            'assigned_to': _('Assigned To'),  # FR: Assigné à
            'start_date': _('Start Date'),  # FR: Date de début
            'end_date': _('End Date'),  # FR: Date de fin
            'status': _('Status'),  # FR: Statut
            'priority': _('Priority'),  # FR: Priorité
            'estimated_hours': _('Estimated Hours'),  # FR: Heures estimées
            'actual_hours': _('Actual Hours'),  # FR: Heures réelles
            'dependencies': _('Dependencies'),  # FR: Dépendances
            'attachments': _('Attachments'),  # FR: Pièces jointes
        }
        
        help_texts = {
            'start_date': _('The date when the task starts.'),  # FR: La date de début de la tâche.
            'end_date': _('The date when the task is expected to end.'),  # FR: La date prévue de fin de la tâche.
            'estimated_hours': _('Estimated number of hours to complete the task.'),  # FR: Nombre d'heures estimé pour terminer la tâche.
            'actual_hours': _('Actual number of hours spent on the task.'),  # FR: Nombre d'heures réellement passées sur la tâche.
            'dependencies': _('Other tasks that need to be completed before this one.'),  # FR: Autres tâches qui doivent être terminées avant celle-ci.
        }
        
        error_messages = {
            'end_date': {
                'invalid': _('End date must be after start date.'),  # FR: La date de fin doit être postérieure à la date de début.
            },
            'estimated_hours': {
                'invalid': _('Estimated hours must be a positive number.'),  # FR: Les heures estimées doivent être un nombre positif.
            },
            'actual_hours': {
                'invalid': _('Actual hours must be a positive number.'),  # FR: Les heures réelles doivent être un nombre positif.
            },
        }
        
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'dependencies': forms.SelectMultiple(),
            'attachments': forms.JSONInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        estimated_hours = cleaned_data.get('estimated_hours')
        actual_hours = cleaned_data.get('actual_hours')

        if start_date and end_date and end_date <= start_date:
            raise forms.ValidationError(_("End date must be after start date."))  # FR: La date de fin doit être postérieure à la date de début.

        if estimated_hours is not None and estimated_hours < 0:
            raise forms.ValidationError(_("Estimated hours must be a positive number."))  # FR: Les heures estimées doivent être un nombre positif.

        if actual_hours is not None and actual_hours < 0:
            raise forms.ValidationError(_("Actual hours must be a positive number."))  # FR: Les heures réelles doivent être un nombre positif.

        return cleaned_data
    
class ProjectResourceForm(forms.ModelForm):
    class Meta:
        model = ProjectResource
        fields = ['project', 'name', 'type', 'quantity', 'unit_cost', 'total_cost', 'availability', 'supplier', 'notes']
        
        labels = {
            'project': _('Project'),  # FR: Projet
            'name': _('Resource Name'),  # FR: Nom de la ressource
            'type': _('Resource Type'),  # FR: Type de ressource
            'quantity': _('Quantity'),  # FR: Quantité
            'unit_cost': _('Unit Cost'),  # FR: Coût unitaire
            'total_cost': _('Total Cost'),  # FR: Coût total
            'availability': _('Availability'),  # FR: Disponibilité
            'supplier': _('Supplier'),  # FR: Fournisseur
            'notes': _('Notes'),  # FR: Notes
        }
        
        help_texts = {
            'type': _('The type of resource (e.g., material, equipment, software).'),  # FR: Le type de ressource (par exemple, matériel, équipement, logiciel).
            'quantity': _('The amount of this resource needed for the project.'),  # FR: La quantité de cette ressource nécessaire pour le projet.
            'unit_cost': _('The cost per unit of this resource.'),  # FR: Le coût par unité de cette ressource.
            'total_cost': _('The total cost for this resource (quantity * unit cost).'),  # FR: Le coût total pour cette ressource (quantité * coût unitaire).
            'availability': _('The availability status of this resource.'),  # FR: Le statut de disponibilité de cette ressource.
        }
        
        error_messages = {
            'quantity': {
                'invalid': _('Quantity must be a positive number.'),  # FR: La quantité doit être un nombre positif.
            },
            'unit_cost': {
                'invalid': _('Unit cost must be a positive number.'),  # FR: Le coût unitaire doit être un nombre positif.
            },
            'total_cost': {
                'invalid': _('Total cost must be a positive number.'),  # FR: Le coût total doit être un nombre positif.
            },
        }
        
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'availability': forms.JSONInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        unit_cost = cleaned_data.get('unit_cost')
        total_cost = cleaned_data.get('total_cost')

        if quantity is not None and quantity < 0:
            raise forms.ValidationError(_("Quantity must be a positive number."))  # FR: La quantité doit être un nombre positif.

        if unit_cost is not None and unit_cost < 0:
            raise forms.ValidationError(_("Unit cost must be a positive number."))  # FR: Le coût unitaire doit être un nombre positif.

        if total_cost is not None and total_cost < 0:
            raise forms.ValidationError(_("Total cost must be a positive number."))  # FR: Le coût total doit être un nombre positif.

        # Verify if total_cost matches quantity * unit_cost
        if quantity is not None and unit_cost is not None and total_cost is not None:
            expected_total_cost = quantity * unit_cost
            if abs(total_cost - expected_total_cost) > 0.01:  # Allow for small floating point discrepancies
                raise forms.ValidationError(_("Total cost should be equal to quantity * unit cost."))  # FR: Le coût total doit être égal à la quantité * le coût unitaire.

        return cleaned_data
    
class ProjectIssueForm(forms.ModelForm):
    class Meta:
        model = ProjectIssue
        fields = ['project', 'reported_by', 'assigned_to', 'title', 'description', 'issue_type', 'priority', 'status', 'resolution', 'due_date', 'resolved_date', 'attachments', 'tags']
        
        labels = {
            'project': _('Project'),  # FR: Projet
            'reported_by': _('Reported By'),  # FR: Signalé par
            'assigned_to': _('Assigned To'),  # FR: Assigné à
            'title': _('Issue Title'),  # FR: Titre du problème
            'description': _('Description'),  # FR: Description
            'issue_type': _('Issue Type'),  # FR: Type de problème
            'priority': _('Priority'),  # FR: Priorité
            'status': _('Status'),  # FR: Statut
            'resolution': _('Resolution'),  # FR: Résolution
            'due_date': _('Due Date'),  # FR: Date d'échéance
            'resolved_date': _('Resolved Date'),  # FR: Date de résolution
            'attachments': _('Attachments'),  # FR: Pièces jointes
            'tags': _('Tags'),  # FR: Étiquettes
        }
        
        help_texts = {
            'due_date': _('The date by which the issue should be resolved.'),  # FR: La date à laquelle le problème devrait être résolu.
            'resolved_date': _('The date when the issue was actually resolved.'),  # FR: La date à laquelle le problème a été effectivement résolu.
            'attachments': _('Any files or documents related to this issue.'),  # FR: Tous les fichiers ou documents liés à ce problème.
            'tags': _('Keywords to categorize and easily find this issue.'),  # FR: Mots-clés pour catégoriser et retrouver facilement ce problème.
        }
        
        error_messages = {
            'due_date': {
                'invalid': _('Due date must be a future date.'),  # FR: La date d'échéance doit être une date future.
            },
            'resolved_date': {
                'invalid': _('Resolved date cannot be earlier than the issue creation date.'),  # FR: La date de résolution ne peut pas être antérieure à la date de création du problème.
            },
        }
        
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'resolution': forms.Textarea(attrs={'rows': 3}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'resolved_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'attachments': forms.JSONInput(),
            'tags': forms.JSONInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        due_date = cleaned_data.get('due_date')
        resolved_date = cleaned_data.get('resolved_date')
        
        if due_date and due_date <= timezone.now():
            raise forms.ValidationError(_("Due date must be a future date."))  # FR: La date d'échéance doit être une date future.
        
        if resolved_date and resolved_date <= self.instance.created_at:
            raise forms.ValidationError(_("Resolved date cannot be earlier than the issue creation date."))  # FR: La date de résolution ne peut pas être antérieure à la date de création du problème.

        return cleaned_data
    
class ProjectTimeEntryForm(forms.ModelForm):
    class Meta:
        model = ProjectTimeEntry
        fields = ['project', 'task', 'user', 'date', 'hours', 'description', 'billable', 'approved']
        
        labels = {
            'project': _('Project'),  # FR: Projet
            'task': _('Task'),  # FR: Tâche
            'user': _('User'),  # FR: Utilisateur
            'date': _('Date'),  # FR: Date
            'hours': _('Hours'),  # FR: Heures
            'description': _('Description'),  # FR: Description
            'billable': _('Billable'),  # FR: Facturable
            'approved': _('Approved'),  # FR: Approuvé
        }
        
        help_texts = {
            'date': _('The date of the time entry.'),  # FR: La date de l'entrée de temps.
            'hours': _('Number of hours worked.'),  # FR: Nombre d'heures travaillées.
            'billable': _('Whether this time is billable to the client.'),  # FR: Si ce temps est facturable au client.
            'approved': _('Whether this time entry has been approved.'),  # FR: Si cette entrée de temps a été approuvée.
        }
        
        error_messages = {
            'hours': {
                'invalid': _('Hours must be a positive number.'),  # FR: Les heures doivent être un nombre positif.
            },
        }
        
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_hours(self):
        hours = self.cleaned_data.get('hours')
        if hours is not None and hours <= 0:
            raise forms.ValidationError(_("Hours must be a positive number."))  # FR: Les heures doivent être un nombre positif.
        return hours

    def clean(self):
        cleaned_data = super().clean()
        project = cleaned_data.get('project')
        task = cleaned_data.get('task')

        if task and project and task.project != project:
            raise forms.ValidationError(_("The selected task does not belong to the selected project."))  # FR: La tâche sélectionnée n'appartient pas au projet sélectionné.

        return cleaned_data