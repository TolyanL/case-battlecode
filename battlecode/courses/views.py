from django.views.generic import ListView, DetailView

from battlecode.pagedata import PageData
from django.db.models import Q
from user.models import Profile
from .models import Course


curr_page = "courses"


class CoursesListView(ListView):
    model = Course
    template_name = "courses_all.html"
    context_object_name = "courses"
    paginate_by = 6

    def get_queryset(self):
        user = self.request.user
        queryset = Course.objects.all()
        if not user.is_authenticated:
            return queryset

        enrolled_ids = Profile.objects.filter(user=user).values_list("courses", flat=True)

        status_filter = self.request.GET.get("enrolled")
        if status_filter == "true":
            return queryset.filter(id__in=enrolled_ids)
        elif status_filter == "false":
            return queryset.exclude(id__in=enrolled_ids)
        else:
            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pd"] = PageData(
            title="All Courses",
            description="",
            curr_page=curr_page,
        )
        context["current_enrolled"] = self.request.GET.get("enrolled", "all")
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
