from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EnrollmentListViewSet,EnrollmentPostViewSet,StudentEnrollmentsView,CourseResultViewSet,EnrolledStudentsView,EditCourseResultViewSet,EnrollmentByStudentAndCourseView

router = DefaultRouter()
router.register('list', EnrollmentListViewSet,basename='enrollment-list')
router.register('enroll',EnrollmentPostViewSet, basename='enrollment-create')
router.register('course-results', CourseResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('my-enrollments/', StudentEnrollmentsView.as_view(), name='student-enrollments'),
    path('students/<int:course_id>/', EnrolledStudentsView.as_view(), name='enrolled-students'),
    path('edit-course-results/<int:pk>/', EditCourseResultViewSet.as_view({'put': 'update'}), name='edit-course-results'),
    path('student/<int:student_id>/course/<int:course_id>/',EnrollmentByStudentAndCourseView.as_view(), name='enrollment-by-student-course'),
]