from django.urls import path
from . import views

urlpatterns = [
    # <str:referral_code> の部分が、RAMEN001などの可変になります
    path('signup/<str:referral_code>/', views.customer_signup, name='customer_signup'),
    path('qrcode/<str:referral_code>/', views.partner_qrcode, name='partner_qrcode'),
]