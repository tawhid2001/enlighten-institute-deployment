from rest_framework import serializers
from .models import Enrollment,CourseResult
from accounts.models import CustomUser


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name']  # Add other fields as necessary


class EnrollmentPostSerailzer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())  # Accepts a user ID

    class Meta:
        model = Enrollment
        fields = ['id', 'enrolled_at', 'student', 'course']

class EnrollmentListSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)  # Nested serializer to include student details

    class Meta:
        model = Enrollment
        fields = ['id', 'enrolled_at', 'student', 'course']

class CourseResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseResult
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']