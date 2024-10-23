from django.db import models
from django.conf import settings
from department.models import Department
from django.db.models import Avg

class Course(models.Model):
    course_name = models.CharField(max_length=200)
    course_code = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    image_url = models.URLField(max_length=255,blank=True,null=True)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, related_name='courses', on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def __str__(self):
        return self.course_name
    
class Review(models.Model):
    course = models.ForeignKey(Course, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # Rating out of 5, for example
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['course', 'user']  # One user can review each course only once

    def __str__(self):
        return f"{self.user} review on {self.course}"

# Add this method in the Course model to calculate average rating
def get_average_rating(self):
    return self.reviews.aggregate(average_rating=Avg('rating'))['average_rating'] or 0


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class LessonProgress(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.OneToOneField(Lesson, related_name='progress', on_delete=models.CASCADE, unique=True)
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} progress on {self.lesson.title}"
