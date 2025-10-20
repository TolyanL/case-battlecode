from django.urls import path

from .views import CoursesListView, CourseDetailView
from .requests import enroll_course, unenroll_course


urlpatterns = [
    path("", CoursesListView.as_view(), name="courses_list"),
    path("<str:slug>", CourseDetailView.as_view(), name="course_detail"),
    # requests
    path("rest/enroll", enroll_course, name="enroll_course"),
    path("rest/unenroll", unenroll_course, name="unenroll_course"),
]

