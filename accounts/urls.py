from django.urls import path
from .views import CustomRegisterView,UserDetailView,ContactView

urlpatterns = [
    path('auth/registration/', CustomRegisterView.as_view(), name='custom-register'),
    path('custom/user/', UserDetailView.as_view(), name='user-detail'),
    path('contact/', ContactView.as_view(), name='contact'),
]
