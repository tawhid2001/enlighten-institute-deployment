from rest_framework import generics, permissions, status
from .serializers import UserUpdateSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from allauth.account.views import ConfirmEmailView
from allauth.account.models import EmailAddress
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render
from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer,CustomUserSerializer,ContactSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail


User = get_user_model()


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    

class CustomConfirmEmailView(ConfirmEmailView):
    template_name = 'email_confirmation_message.html'

    def get(self, request, *args, **kwargs):
        key = kwargs['key']
        try:
            uidb64, token = key.split(':')
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            email_address = EmailAddress.objects.get(user=user)
            if default_token_generator.check_token(user, token) and not email_address.verified:
                email_address.verified = True
                email_address.save()
                user.is_active = True
                user.save()
                return HttpResponse('Email confirmed and account activated.', status=200)
            else:
                return HttpResponse('Invalid confirmation link or user already activated.', status=400)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, EmailAddress.DoesNotExist):
            return HttpResponse('Invalid confirmation link.', status=400)

def account_inactive(request):
    return render(request, 'account_inactive.html')

class ContactView(APIView):
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            message = serializer.validated_data['message']
            admin_email = '211003042.primeasia@gmail.com'  # Set your admin email here
            
            # Send the email
            try:
                send_mail(
                    subject='Contact Form Submission',
                    message=f"Message from: {email}\n\n{message}",
                    from_email=email,  # From email (user's email)
                    recipient_list=[admin_email],  # To email (admin's email)
                )
                return Response({'status': 'Message sent!'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'status': 'Error sending message.', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)