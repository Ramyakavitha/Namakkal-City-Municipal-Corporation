from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.RegisterComplaintView.as_view(), name='register_complaint'),
    path('check-status/', views.CheckStatusView.as_view(), name='check_status'),
    path('complaint/<slug:complaint_number>/', views.ComplaintDetailView.as_view(), name='complaint_detail'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    
    # Redesigned Dashboard Admin Panel
    path('dashboard/', views.AdminDashboardIndexView.as_view(), name='dashboard_index'),
    path('dashboard/login/', views.AdminLoginView.as_view(), name='dashboard_login'),
    path('dashboard/logout/', views.AdminLogoutView.as_view(), name='dashboard_logout'),
    path('dashboard/complaints/', views.AdminComplaintsListView.as_view(), name='dashboard_complaints'),
    path('dashboard/register-complaint/', views.AdminRegisterComplaintView.as_view(), name='dashboard_register_complaint'),
    path('dashboard/conversations/', views.AdminConversationsView.as_view(), name='dashboard_conversations'),
    path('dashboard/template-status/', views.AdminTemplateStatusView.as_view(), name='dashboard_template_status'),
    path('dashboard/template-manager/', views.AdminTemplateManagerView.as_view(), name='dashboard_template_manager'),
    path('dashboard/campaigns/', views.AdminCampaignsView.as_view(), name='dashboard_campaigns'),
    path('dashboard/departments/', views.AdminDepartmentsView.as_view(), name='dashboard_departments'),
    path('dashboard/agent-accounts/', views.AdminAgentAccountsView.as_view(), name='dashboard_agent_accounts'),
    path('dashboard/news/', views.AdminNewsView.as_view(), name='dashboard_news'),

    # Legacy / compatibility URLs
    path('complaints-admin/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('complaints-admin/<slug:complaint_number>/', views.AdminComplaintDetailView.as_view(), name='admin_complaint_detail'),
    path('complaints-admin/export/excel/', views.ExportComplaintsExcelView.as_view(), name='export_excel'),
    
    # AJAX Endpoints
    path('ajax/send-otp/', views.SendOTPView.as_view(), name='send_otp'),
    path('ajax/verify-otp/', views.VerifyOTPView.as_view(), name='verify_otp'),
    path('ajax/get-wards-areas/', views.GetWardsAreasView.as_view(), name='get_wards_areas'),
]
