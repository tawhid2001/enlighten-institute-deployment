from django.shortcuts import get_object_or_404
from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Enrollment,CourseResult
from .serializers import EnrollmentListSerializer,EnrollmentPostSerailzer,CourseResultSerializer
from rest_framework.permissions import IsAuthenticated
from course.models import Course

# Create your views here.

class EnrollmentListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentListSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Enrollment.objects.filter(student=self.request.user)
        return Enrollment.objects.none()
    
class EnrollmentPostViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentPostSerailzer

    def create(self, request, *args, **kwargs):
        student = request.user
        course_id = request.data.get('course')
        if Enrollment.objects.filter(student=student, course_id=course_id).exists():
            return Response({'detail': 'Already enrolled in this course.'}, status=status.HTTP_400_BAD_REQUEST)

        data = {'student': student.id, 'course': course_id}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class StudentEnrollmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        student = request.user
        enrollments = Enrollment.objects.filter(student=student)
        serializer = EnrollmentListSerializer(enrollments, many=True)
        return Response(serializer.data)
    

class EnrolledStudentsView(APIView):

    def get(self, request, course_id, *args, **kwargs):
        enrollments = Enrollment.objects.filter(course_id=course_id)
        serializer = EnrollmentListSerializer(enrollments, many=True)
        return Response(serializer.data)
    
class CourseResultViewSet(viewsets.ModelViewSet):
    queryset = CourseResult.objects.all()
    serializer_class = CourseResultSerializer

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'teacher':
            return CourseResult.objects.filter(enrollment__course__teacher=user)
        elif user.user_type == 'student':
            return CourseResult.objects.filter(enrollment__student=user)
        return CourseResult.objects.none()
    
    
class EditCourseResultViewSet(viewsets.ViewSet):
    serializer_class = CourseResultSerializer

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'teacher':
            return CourseResult.objects.filter(enrollment__course__teacher=user)
        elif user.user_type == 'student':
            return CourseResult.objects.filter(enrollment__student=user)
        return CourseResult.objects.none()

    def update(self, request, pk=None):
        queryset = self.get_queryset()
        try:
            instance = queryset.get(pk=pk)
        except CourseResult.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


class EnrollmentByStudentAndCourseView(APIView):
    def get(self, request, student_id, course_id):
        try:
            enrollment = Enrollment.objects.get(student_id=student_id, course_id=course_id)
            serializer = EnrollmentPostSerailzer(enrollment)
            return Response(serializer.data)
        except Enrollment.DoesNotExist:
            return Response({"error": "Enrollment not found"}, status=404)