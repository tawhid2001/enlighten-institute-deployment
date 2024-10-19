from rest_framework import serializers
from .models import Course,Lesson,LessonProgress



class CourseListSerializer(serializers.ModelSerializer):
    teacher_name = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()
    image_url = serializers.CharField(required=False,allow_blank=True)
    class Meta:
        model = Course
        fields = ['id', 'course_name', 'course_code', 'description', 'image_url' ,'created_at', 'slug', 'teacher', 'teacher_name', 'department', 'department_name']

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