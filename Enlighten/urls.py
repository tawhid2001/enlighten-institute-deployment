"""Enlighten URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from accounts.views import CustomConfirmEmailView,account_inactive
from django.conf import settings
from django.conf.urls.static import static
from payment.views import create_checkout_session,stripe_webhook,get_publishable_key,success_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/course/', include('course.urls')),
    path('api/department/', include('department.urls')),
    path('api/enrollment/', include('enrollment.urls')),
    # path('api/payment/', include('payment.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/auth/', include("dj_rest_auth.urls")),
    # path('api/auth/registration/', include("dj_rest_auth.registration.urls")),
    path('api/auth/registration/account_confirm_email/<str:key>/', CustomConfirmEmailView.as_view(), 
    name='account_confirm_email'),
    path('account/inactive/', account_inactive, name="account_inactive"),
    path('api/', include("accounts.urls")),
    path('create-checkout-session/', create_checkout_session, name='create-checkout-session'),
    path('stripe_webhook/', stripe_webhook, name='stripe-webhook'),
    path('get-publishable-key/', get_publishable_key, name='get-publishable-key'), 
    path('success/', success_view, name='success'), 
]
