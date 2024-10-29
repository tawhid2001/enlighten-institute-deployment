from rest_framework import serializers
from .models import Course,Lesson,LessonProgress,Review
from django.contrib.auth import get_user_model


class CourseListSerializer(serializers.ModelSerializer):
    teacher_name = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()
    image_url = serializers.CharField(required=False,allow_blank=True)
    average_rating = serializers.FloatField(read_only=True)  # Include the average rating field
    class Meta:
        model = Course
        fields = ['id', 'course_name', 'course_code', 'description', 'image_url' ,'created_at', 'slug', 'teacher', 'teacher_name', 'department', 'department_name','average_rating','price']

        read_only_fields = ["teacher",]

    def create(self,validated_data):
        image_url = validated_data.pop('image_url',None)
        course = Course.objects.create(**validated_data)
        if image_url:
            course.image_url = image_url
            course.save()
        return course

    def get_teacher_name(self, obj):
        return obj.teacher.get_full_name() or obj.teacher.username

    def get_department_name(self, obj):
        return obj.department.name
    
  
    
    
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
    
class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = '__all__'


class ProgressSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    course_name = serializers.CharField()
    progress = serializers.FloatField()

# Get the user model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # Add any other fields you'd like to expose

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Nest the UserSerializer
    class Meta:
        model = Review
        fields = ['id', 'course', 'rating', 'comment', 'user', 'created_at']  # Include 'user' field for user details

    def validate(self, data):
        user = self.context['request'].user
        course = data.get('course')
        review_id = self.instance.id if self.instance else None  # Get the review ID if updating

        # Check if a review for the course by the same user exists, excluding the current review
        if Review.objects.filter(course=course, user=user).exclude(id=review_id).exists():
            raise serializers.ValidationError("You have already reviewed this course.")
        return data

  

    