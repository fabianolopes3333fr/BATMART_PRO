from django.urls import path
from .views import DashboardCreateView, DashboardDeleteView, DashboardDetailView, DashboardListView, DashboardUpdateView, MetricCreateView, MetricDeleteView, MetricDetailView, MetricListView, MetricUpdateView, ReportExecutionCreateView, ReportExecutionDeleteView, ReportExecutionDetailView, ReportExecutionListView, ReportExecutionUpdateView, ReportListView, ReportCreateView, ReportDetailView, ReportUpdateView, ReportDeleteView

app_name = 'analytics'

urlpatterns = [
    path('reports/', ReportListView.as_view(), name='report_list'),
    path('reports/create/', ReportCreateView.as_view(), name='report_create'),
    path('reports/<int:pk>/', ReportDetailView.as_view(), name='report_detail'),
    path('reports/<int:pk>/update/', ReportUpdateView.as_view(), name='report_update'),
    path('reports/<int:pk>/delete/', ReportDeleteView.as_view(), name='report_delete'),
    
    path('report-executions/', ReportExecutionListView.as_view(), name='report_execution_list'),
    path('report-executions/create/', ReportExecutionCreateView.as_view(), name='report_execution_create'),
    path('report-executions/<int:pk>/', ReportExecutionDetailView.as_view(), name='report_execution_detail'),
    path('report-executions/<int:pk>/update/', ReportExecutionUpdateView.as_view(), name='report_execution_update'),
    path('report-executions/<int:pk>/delete/', ReportExecutionDeleteView.as_view(), name='report_execution_delete'),
    
    path('dashboards/', DashboardListView.as_view(), name='dashboard_list'),
    path('dashboards/create/', DashboardCreateView.as_view(), name='dashboard_create'),
    path('dashboards/<int:pk>/', DashboardDetailView.as_view(), name='dashboard_detail'),
    path('dashboards/<int:pk>/update/', DashboardUpdateView.as_view(), name='dashboard_update'),
    path('dashboards/<int:pk>/delete/', DashboardDeleteView.as_view(), name='dashboard_delete'),
    
    path('metrics/', MetricListView.as_view(), name='metric_list'),
    path('metrics/create/', MetricCreateView.as_view(), name='metric_create'),
    path('metrics/<int:pk>/', MetricDetailView.as_view(), name='metric_detail'),
    path('metrics/<int:pk>/update/', MetricUpdateView.as_view(), name='metric_update'),
    path('metrics/<int:pk>/delete/', MetricDeleteView.as_view(), name='metric_delete'),
]