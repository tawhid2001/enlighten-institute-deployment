# payment/views.py
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from course.models import Course  # Import your Course model
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from enrollment.models import Enrollment  # Import Enrollment to create it on payment success
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

stripe.api_key = settings.STRIPE_SECRET_KEY

import logging

logger = logging.getLogger(__name__)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):
    try:
        course_id = request.data.get("course_id")
        if not course_id:
            logger.error("Course ID not provided")
            return Response({"error": "Course ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(id=course_id)
            amount = int(course.price * 100)
        except Course.DoesNotExist:
            logger.error(f"Course with ID {course_id} not found")
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'Course: {course.course_name}',
                            'image': course.image_url,
                        },
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url="",  # Your success URL
            cancel_url="",
            metadata={
                "course_id": course_id,
                "student_id": request.user.id,
            },
        )
        return Response({'id': checkout_session.id})

    except Exception as e:
        logger.exception("An error occurred while creating the checkout session")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
@csrf_exempt
@api_view(['POST'])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return Response(status=400)

    # Process only specific events
    if event['type'] == 'checkout.session.completed':
        payment_intent_id = event['data']['object']['payment_intent']
        process_payment.delay(payment_intent_id)  # Defer to background task
    return Response(status=200)  # Acknowledge quickly


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_publishable_key(request):
    return JsonResponse({"publishable_key": settings.STRIPE_PUBLISHABLE_KEY})

