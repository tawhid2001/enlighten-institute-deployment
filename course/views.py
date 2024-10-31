from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status,viewsets
from .models import Course,Lesson,LessonProgress,Review
from .serializers import CourseListSerializer,LessonProgressSerializer,ProgressSerializer,LessonSerializer,ReviewSerializer
from django.http import Http404
from .permissions import IsTeacherrOrReadOnly
from rest_framework.permissions import IsAuthenticated,AllowAny
import requests
from rest_framework.response import Response
from django.db.models import Avg

# Create your views here.


class CourseList(APIView):
    permission_classes = [IsAuthenticated, IsTeacherrOrReadOnly]

    def get(self, request, format=None):
        user = request.user
        if user.user_type == 'teacher':
            courses = Course.objects.filter(teacher=user)
        else:
            courses = Course.objects.all()
        serializer = CourseListSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data.copy()
        data['teacher'] = request.user.id  # Associate the course with the logged-in teacher

        # Handling image upload to Imgbb
        image = request.FILES.get('image')
        if image:
            imgbb_api_key = '74a46b9f674cfe097a70c2c8824668a7'
            imgbb_response = requests.post(
                f"https://api.imgbb.com/1/upload?key={imgbb_api_key}",
                files={'image': image}
            )
            print(imgbb_response.json())  # Debugging: print full Imgbb response
            if imgbb_response.status_code == 200:
                image_url = imgbb_response.json().get('data', {}).get('url')
                print(f"Image URL: {image_url}")  # Debugging: print extracted URL
                if image_url:
                    data['image_url'] = image_url
            else:
                return Response({"error": "Image upload failed"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CourseListSerializer(data=data)

        if serializer.is_valid():
            serializer.save(teacher=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class CourseDetail(APIView):
    # permission_classes = [IsTeacherrOrReadOnly]
    def get_object(self,pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404
        
    def get(self,request,pk,format=None):
        course = self.get_object(pk)
        serializer = CourseListSerializer(course)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        course = self.get_object(pk)
        data = request.data.copy()

        # Check if a new image is being uploaded
        image = request.FILES.get('image')
        if image:
            imgbb_api_key = '74a46b9f674cfe097a70c2c8824668a7'
            imgbb_response = requests.post(
                f"https://api.imgbb.com/1/upload?key={imgbb_api_key}",
                files={'image': image}
            )
            
            # Debugging: print Imgbb response to verify image upload
            print(imgbb_response.json())
            
            if imgbb_response.status_code == 200:
                image_url = imgbb_response.json().get('data', {}).get('url')
                print(f"New Image URL: {image_url}")
                if image_url:
                    data['image_url'] = image_url  # Update the image URL in the data
            else:
                return Response({"error": "Image upload failed"}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize and update the course
        serializer = CourseListSerializer(course, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self,request,pk,format=None):
        course =self.get_object(pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class LessonViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsTeacherrOrReadOnly]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonListCreate(APIView):
    def get(self, request, course_id, format=None):
        lessons = Lesson.objects.filter(course_id=course_id)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)

    def post(self, request, course_id, format=None):
        data = request.data
        data['course'] = course_id
        serializer = LessonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LessonDetails(APIView):
    def get_object(self,pk):
        try:
            return Lesson.objects.get(pk=pk)
        except Lesson.DoesNotExist:
            raise Http404
        
    def get(self,request,pk,format=None):
        lesson = self.get_object(pk)
        serializer = LessonSerializer(lesson)
        return Response(serializer.data)
    
    def put(self,request,pk,format=None):
        lesson = self.get_object(pk)
        serializer = LessonSerializer(lesson,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk,format=None):
        lesson =self.get_object(pk)
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


class LessonProgressViewSet(viewsets.ModelViewSet):
    queryset = LessonProgress.objects.all()
    serializer_class = LessonProgressSerializer


class CourseLessonsWithProgress(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        course = get_object_or_404(Course, pk=pk)
        lessons = course.lessons.all()
        user = request.user

        lessons_data = []
        for lesson in lessons:
            progress = LessonProgress.objects.filter(lesson=lesson, student=user).first()
            lesson_data = {
                'id': lesson.id,
                'title': lesson.title,
                'content': lesson.content,
                'created_at': lesson.created_at,
                'completed': progress.completed if progress else False,
            }
            lessons_data.append(lesson_data)

        return Response(lessons_data)

class CourseProgressView(APIView):
    def get(self, request, course_id):
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        total_lessons = course.lessons.count()
        if total_lessons == 0:
            progress_percentage = 0
        else:
            completed_lessons = LessonProgress.objects.filter(student=user, lesson__course=course, completed=True).count()
            progress_percentage = (completed_lessons / total_lessons) * 100

        progress_data = {
            'course_id': course.id,
            'course_name': course.course_name,
            'progress': progress_percentage
        }

        serializer = ProgressSerializer(progress_data)
        return Response(serializer.data)
    
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # Allow anyone to view reviews
            return [AllowAny()]
        # Only authenticated users can create, update, or delete reviews
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        # Automatically associate the logged-in user with the review
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        # Allow only the owner of the review to update it
        review = self.get_object()
        if review.user != request.user:
            return Response({"detail": "You do not have permission to edit this review."}, status=403)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        # Allow only the owner of the review to delete it
        review = self.get_object()
        if review.user != request.user:
            return Response({"detail": "You do not have permission to delete this review."}, status=403)
        return super().destroy(request, *args, **kwargs)
    
class TopRatedCoursesView(APIView):
    def get(self, request):
        # Fetch top 3 courses with an average rating, excluding courses with no reviews
        top_courses = (
            Course.objects
            .annotate(average_rating=Avg('reviews__rating'))
            .filter(average_rating__isnull=False)  # Exclude courses without reviews
            .order_by('-average_rating')[:3]
        )

        serializer = CourseListSerializer(top_courses, many=True)
        return Response(serializer.data)
