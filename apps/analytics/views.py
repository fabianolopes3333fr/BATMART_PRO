from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Report, ReportExecution, Dashboard, Metric, Alert, DataExport
from .forms import ReportForm, ReportExecutionForm, DashboardForm, MetricForm, AlertForm, DataExportForm

class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'analytics/report_list.html'
    context_object_name = 'report_list'

    def get_queryset(self):
        return Report.objects.filter(company=self.request.user.company)

class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'analytics/report_detail.html'
    context_object_name = 'report'

class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'analytics/report_form.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        form.instance.created_by = self.request.user
        messages.success(self.request, _('Report created successfully.'))
        return super().form_valid(form)

class ReportUpdateView(LoginRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'analytics/report_form.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        messages.success(self.request, _('Report updated successfully.'))
        return super().form_valid(form)

class ReportDeleteView(LoginRequiredMixin, DeleteView):
    model = Report
    template_name = 'analytics/report_confirm_delete.html'
    success_url = reverse_lazy('analytics:report_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _('Report deleted successfully.'))
        return super().delete(request, *args, **kwargs)
    
    
class ReportExecutionListView(LoginRequiredMixin, ListView):
    model = ReportExecution
    template_name = 'analytics/report_execution_list.html'
    context_object_name = 'report_executions'

    def get_queryset(self):
        return ReportExecution.objects.filter(report__company=self.request.user.company)

class ReportExecutionDetailView(LoginRequiredMixin, DetailView):
    model = ReportExecution
    template_name = 'analytics/report_execution_detail.html'
    context_object_name = 'report_execution'

class ReportExecutionCreateView(LoginRequiredMixin, CreateView):
    model = ReportExecution
    form_class = ReportExecutionForm
    template_name = 'analytics/report_execution_form.html'
    success_url = reverse_lazy('analytics:report_execution_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, _("Report execution created successfully."))
        # Traduction française: "L'exécution du rapport a été créée avec succès."
        return super().form_valid(form)

class ReportExecutionUpdateView(LoginRequiredMixin, UpdateView):
    model = ReportExecution
    form_class = ReportExecutionForm
    template_name = 'analytics/report_execution_form.html'
    success_url = reverse_lazy('analytics:report_execution_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, _("Report execution updated successfully."))
        # Traduction française: "L'exécution du rapport a été mise à jour avec succès."
        return super().form_valid(form)

class ReportExecutionDeleteView(LoginRequiredMixin, DeleteView):
    model = ReportExecution
    template_name = 'analytics/report_execution_confirm_delete.html'
    success_url = reverse_lazy('analytics:report_execution_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _("Report execution deleted successfully."))
        # Traduction française: "L'exécution du rapport a été supprimée avec succès."
        return super().delete(request, *args, **kwargs)

# Add these translations to your translation files
_("Report execution created successfully.")
_("Report execution updated successfully.")
_("Report execution deleted successfully.")

class DashboardListView(LoginRequiredMixin, ListView):
    model = Dashboard
    template_name = 'analytics/dashboard_list.html'
    context_object_name = 'dashboards'

    def get_queryset(self):
        return Dashboard.objects.filter(company=self.request.user.company)

class DashboardDetailView(LoginRequiredMixin, DetailView):
    model = Dashboard
    template_name = 'analytics/dashboard_detail.html'
    context_object_name = 'dashboard'

class DashboardCreateView(LoginRequiredMixin, CreateView):
    model = Dashboard
    form_class = DashboardForm
    template_name = 'analytics/dashboard_form.html'
    success_url = reverse_lazy('analytics:dashboard_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, _("Dashboard created successfully."))
        # French translation: "Le tableau de bord a été créé avec succès."
        return super().form_valid(form)

class DashboardUpdateView(LoginRequiredMixin, UpdateView):
    model = Dashboard
    form_class = DashboardForm
    template_name = 'analytics/dashboard_form.html'
    success_url = reverse_lazy('analytics:dashboard_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, _("Dashboard updated successfully."))
        # French translation: "Le tableau de bord a été mis à jour avec succès."
        return super().form_valid(form)

class DashboardDeleteView(LoginRequiredMixin, DeleteView):
    model = Dashboard
    template_name = 'analytics/dashboard_confirm_delete.html'
    success_url = reverse_lazy('analytics:dashboard_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _("Dashboard deleted successfully."))
        # French translation: "Le tableau de bord a été supprimé avec succès."
        return super().delete(request, *args, **kwargs)

# Add these translations to your translation files
_("Dashboard created successfully.")
_("Dashboard updated successfully.")
_("Dashboard deleted successfully.")

class MetricListView(LoginRequiredMixin, ListView):
    model = Metric
    template_name = 'analytics/metric_list.html'
    context_object_name = 'metrics'

    def get_queryset(self):
        return Metric.objects.filter(company=self.request.user.company)

class MetricDetailView(LoginRequiredMixin, DetailView):
    model = Metric
    template_name = 'analytics/metric_detail.html'
    context_object_name = 'metric'

class MetricCreateView(LoginRequiredMixin, CreateView):
    model = Metric
    form_class = MetricForm
    template_name = 'analytics/metric_form.html'
    success_url = reverse_lazy('analytics:metric_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        messages.success(self.request, _("Metric created successfully."))
        # French translation: "La métrique a été créée avec succès."
        return super().form_valid(form)

class MetricUpdateView(LoginRequiredMixin, UpdateView):
    model = Metric
    form_class = MetricForm
    template_name = 'analytics/metric_form.html'
    success_url = reverse_lazy('analytics:metric_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, _("Metric updated successfully."))
        # French translation: "La métrique a été mise à jour avec succès."
        return super().form_valid(form)

class MetricDeleteView(LoginRequiredMixin, DeleteView):
    model = Metric
    template_name = 'analytics/metric_confirm_delete.html'
    success_url = reverse_lazy('analytics:metric_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _("Metric deleted successfully."))
        # French translation: "La métrique a été supprimée avec succès."
        return super().delete(request, *args, **kwargs)

# Add these translations to your translation files
_("Metric created successfully.")
_("Metric updated successfully.")
_("Metric deleted successfully.")

class AlertListView(LoginRequiredMixin, ListView):
    model = Alert
    template_name = 'analytics/alert_list.html'
    context_object_name = 'alerts'

    def get_queryset(self):
        return Alert.objects.filter(company=self.request.user.company)

class AlertDetailView(LoginRequiredMixin, DetailView):
    model = Alert
    template_name = 'analytics/alert_detail.html'
    context_object_name = 'alert'

class AlertCreateView(LoginRequiredMixin, CreateView):
    model = Alert
    form_class = AlertForm
    template_name = 'analytics/alert_form.html'
    success_url = reverse_lazy('analytics:alert_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        messages.success(self.request, _("Alert created successfully."))
        # French translation: "L'alerte a été créée avec succès."
        return super().form_valid(form)

class AlertUpdateView(LoginRequiredMixin, UpdateView):
    model = Alert
    form_class = AlertForm
    template_name = 'analytics/alert_form.html'
    success_url = reverse_lazy('analytics:alert_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, _("Alert updated successfully."))
        # French translation: "L'alerte a été mise à jour avec succès."
        return super().form_valid(form)

class AlertDeleteView(LoginRequiredMixin, DeleteView):
    model = Alert
    template_name = 'analytics/alert_confirm_delete.html'
    success_url = reverse_lazy('analytics:alert_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _("Alert deleted successfully."))
        # French translation: "L'alerte a été supprimée avec succès."
        return super().delete(request, *args, **kwargs)

# Add these translations to your translation files
_("Alert created successfully.")
_("Alert updated successfully.")
_("Alert deleted successfully.")


class DataExportListView(LoginRequiredMixin, ListView):
    model = DataExport
    template_name = 'analytics/data_export_list.html'
    context_object_name = 'data_exports'

    def get_queryset(self):
        return DataExport.objects.filter(company=self.request.user.company)

class DataExportDetailView(LoginRequiredMixin, DetailView):
    model = DataExport
    template_name = 'analytics/data_export_detail.html'
    context_object_name = 'data_export'

class DataExportCreateView(LoginRequiredMixin, CreateView):
    model = DataExport
    form_class = DataExportForm
    template_name = 'analytics/data_export_form.html'
    success_url = reverse_lazy('analytics:data_export_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        form.instance.created_by = self.request.user.companyuser
        messages.success(self.request, _("Data export created successfully."))
        # French translation: "L'exportation de données a été créée avec succès."
        return super().form_valid(form)

class DataExportUpdateView(LoginRequiredMixin, UpdateView):
    model = DataExport
    form_class = DataExportForm
    template_name = 'analytics/data_export_form.html'
    success_url = reverse_lazy('analytics:data_export_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, _("Data export updated successfully."))
        # French translation: "L'exportation de données a été mise à jour avec succès."
        return super().form_valid(form)

class DataExportDeleteView(LoginRequiredMixin, DeleteView):
    model = DataExport
    template_name = 'analytics/data_export_confirm_delete.html'
    success_url = reverse_lazy('analytics:data_export_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _("Data export deleted successfully."))
        # French translation: "L'exportation de données a été supprimée avec succès."
        return super().delete(request, *args, **kwargs)

# Add these translations to your translation files
_("Data export created successfully.")
_("Data export updated successfully.")
_("Data export deleted successfully.")