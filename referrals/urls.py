from django.urls import path
from . import views

urlpatterns = [
    # <str:referral_code> の部分が、RAMEN001などの可変になります
    path('signup/<str:referral_code>/', views.customer_signup, name='customer_signup'),
    path('qrcode/<str:referral_code>/', views.partner_qrcode, name='partner_qrcode'),
    path('dashboard/', views.dashboard_stats, name='dashboard_stats'),
    path('partner/login/', views.partner_login, name='partner_login'),
    path('partner/dashboard/', views.partner_dashboard, name='partner_dashboard'),
    path('partner/logout/', views.partner_logout, name='partner_logout'),
]