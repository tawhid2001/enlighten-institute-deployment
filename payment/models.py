from django.db import models
from django.conf import settings
from course.models import Course

# Create your models here.
class Payment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default="pending")  # e.g., 'pending', 'succeeded', 'failed'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.course.course_name} - {self.status}"
