from django.conf import settings
from django.db import models
from course.models import Course


class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')  # Ensure a student can enroll in a course only once

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.course_name}"


class CourseResult(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    marks = models.DecimalField(max_digits=5, decimal_places=2)
    feedback = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('enrollment',)

    def __str__(self):
        return f"{self.enrollment.student.first_name} - {self.enrollment.course.course_name}: {self.marks}"