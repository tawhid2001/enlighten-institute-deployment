from django.urls import path
from .views import DepartmentViewset,DepartmentCourseViewSet

urlpatterns = [
    path('courselist/',DepartmentViewset.as_view({'get': 'list'})),
    path('courselist/<slug:slug>/',DepartmentCourseViewSet.as_view()),
]