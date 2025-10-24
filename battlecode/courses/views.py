# battlecode/courses/views.py
from django.views.generic import ListView, DetailView
from django.db.models import Q
from battlecode.pagedata import PageData
from user.models import Profile
from peer_review.models import Assignment
from .models import Course

curr_page = "courses"

class CoursesListView(ListView):
    model = Course
    template_name = "courses_all.html"
    context_object_name = "courses"
    paginate_by = 6

    def get_queryset(self):
        queryset = Course.objects.all().order_by('created_at')
        user = self.request.user
        if not user.is_authenticated:
            return queryset

        enrolled_ids = Profile.objects.filter(user=user).values_list("courses", flat=True)

        status_filter = self.request.GET.get("status")
        if status_filter == "enrolled":
            completed_ids = self._get_completed_course_ids(user, queryset.filter(id__in=enrolled_ids))
            return queryset.filter(id__in=enrolled_ids).exclude(id__in=completed_ids)
        elif status_filter == "available":
            return queryset.exclude(id__in=enrolled_ids)
        elif status_filter == "completed":
            completed_ids = self._get_completed_course_ids(user, queryset.filter(id__in=enrolled_ids))
            return queryset.filter(id__in=completed_ids)
        else:
            return queryset

    def _get_completed_course_ids(self, user, courses_qs):
        completed_ids = []
        for course in courses_qs:
            total = course.quests.count()
            if total == 0:
                completed_ids.append(course.id)
            else:
                success_count = Assignment.objects.filter(
                    user=user,
                    quest__in=course.quests.all(),
                    status="success"
                ).count()
                if success_count == total:
                    completed_ids.append(course.id)
        return completed_ids

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["pd"] = PageData(
            title="All Courses",
            description="",
            curr_page=curr_page,
        )
        context["current_status"] = self.request.GET.get("status", "all")

        # Передаём список завершённых курсов для скрытия кнопки
        if user.is_authenticated:
            enrolled_courses = Profile.objects.filter(user=user).values_list("courses", flat=True)
            context["completed_course_ids"] = set(self._get_completed_course_ids(user, Course.objects.filter(id__in=enrolled_courses)))
        else:
            context["completed_course_ids"] = set()

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
        user = self.request.user
        course = self.object

        accepted = False
        course_completed = False

        if user.is_authenticated:
            accepted = Profile.objects.filter(user=user, courses=course).exists()
            if accepted:
                total = course.quests.count()
                if total > 0:
                    success_count = Assignment.objects.filter(
                        user=user,
                        quest__in=course.quests.all(),
                        status="success"
                    ).count()
                    course_completed = (success_count == total)
                else:
                    course_completed = True

        context["accepted"] = accepted
        context["course_completed"] = course_completed
        return context