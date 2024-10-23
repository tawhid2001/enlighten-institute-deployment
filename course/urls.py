from django.urls import path,include
from .views import CourseList,CourseDetail,CourseProgressView,CourseLessonsWithProgress,LessonProgressViewSet,LessonDetails,LessonListCreate,ReviewViewSet,TopRatedCoursesView

urlpatterns = [
    path('courselist/', CourseList.as_view(),name="course_list"),
    path('courselist/<int:pk>/', CourseDetail.as_view(),name="course_detail"),
    path('<int:course_id>/lessons/', LessonListCreate.as_view(), name='lesson-list-create'),
    path('course_progress/<int:course_id>/', CourseProgressView.as_view(), name='course_progress'),
    path('courselessons/<int:pk>/', CourseLessonsWithProgress.as_view(),name="course_lessons"),
    path('lesson/<int:pk>/', LessonDetails.as_view(),name="lesson_detail"),
    path('lessonprogress/',LessonProgressViewSet.as_view({'get': 'list', 'post': 'create'}),name="lesson-progress"),
    path('review/',ReviewViewSet.as_view({'get': 'list', 'post': 'create'}), name="reviews"),
    path('top-rated-courses/',TopRatedCoursesView.as_view(),name='top-rated-courses'),
]