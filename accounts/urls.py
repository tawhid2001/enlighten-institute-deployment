from django.urls import path
from .views import CustomRegisterView

urlpatterns = [
    path('auth/registration/', CustomRegisterView.as_view(), name='custom-register'),
]
