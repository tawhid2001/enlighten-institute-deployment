from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DepartmentSerializer
from course.serializers import CourseListSerializer
from .models import Department
from rest_framework import viewsets
# Create your views here.


class DepartmentViewset(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentCourseViewSet(APIView):
    def get(self, request, slug=None):
        department = get_object_or_404(Department, slug = slug)
        courses = department.courses.all()
        serializer = CourseListSerializer(courses, many=True)
        return Response(serializer.data)