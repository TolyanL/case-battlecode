from django.views.generic import ListView, DetailView

from battlecode.pagedata import PageData

from user.models import Profile
from .models import Course


curr_page = "courses"


class CoursesListView(ListView):
    model = Course
    template_name = "courses_all.html"
    context_object_name = "courses"

    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pd"] = PageData(
            title="All Courses",
            description="",
            curr_page=curr_page,
        )

        return context


class CourseDetailView(DetailView):
    model = Course
    template_name = "course_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pd"] = PageData(
            title=f"Курс {self.object.title}",
            description="",
            curr_page=curr_page,
        )

        context["accepted"] = Profile.objects.filter(
            user=self.request.user,
            courses=self.object,
        ).exists()

        return context
