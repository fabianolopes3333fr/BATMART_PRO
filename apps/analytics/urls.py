from django.urls import path
from .views import ReportExecutionCreateView, ReportExecutionDeleteView, ReportExecutionDetailView, ReportExecutionListView, ReportExecutionUpdateView, ReportListView, ReportCreateView, ReportDetailView, ReportUpdateView, ReportDeleteView

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
]