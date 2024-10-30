# payment/urls.py
from django.urls import path
from payment.views import create_checkout_session,stripe_webhook,get_publishable_key
urlpatterns = [
    path('stripe-webhook/', stripe_webhook, name='stripe-webhook'),
    path('get-publishable-key/', get_publishable_key, name='get-publishable-key'), 
]
