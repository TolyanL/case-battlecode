from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Q

from battlecode.pagedata import PageData
from battlecode.quest_settings import break_delta

from user.models import Profile
from peer_review.models import Assignment
from courses.models import Course


curr_page = "courses"


class CoursesListView(ListView):
    model = Course
    template_name = "courses_all.html"
    context_object_name = "courses"

    paginate_by = 6

    def get_queryset(self):
        courses = Course.objects.filter(active=True).all()

        user = self.request.user

        if user.is_authenticated:
            for c in courses:
                finished_quests = (
                    c.quests.filter(
                        assignments__user=user,
                        assignments__assigned_at__gte=break_delta(),
                    )
                    .filter(Q(assignments__status="success") | Q(assignments__status="failed"))
                    .count()
                )
                c.progress = int(100 * finished_quests / c.quests.count())
                if c.progress > 100:
                    c.progress = 100

                if user.profile.courses.filter(id=c.id).exists():
                    c.enrolled = True

        return courses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pd"] = PageData(
            title="All Courses",
            description="",
            curr_page=curr_page,
        )

        return context


class CourseDetailView(DetailView, LoginRequiredMixin):
    model = Course
    template_name = "course_detail.html"

    def get_object(self):
        c = super().get_object()

        success_quests = c.quests.filter(
            assignments__user=self.request.user,
            assignments__status="success",
        ).count()
        c.progress = int(100 * success_quests / c.quests.count())

        return c

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["pd"] = PageData(
            title=f"Курс {self.object.title}",
            description="",
            curr_page=curr_page,
        )

        context["is_accepted"] = Profile.objects.filter(
            user=user,
            courses=self.object,
        ).exists()

        if user.is_authenticated:
            context["accepted"] = (
                Assignment.objects.filter(user=user).filter(status="active").values_list("quest__slug", flat=True)
            )

            context["review"] = (
                Assignment.objects.filter(user=user).filter(status="completed").values_list("quest__slug", flat=True)
            )
            context["completed"] = (
                Assignment.objects.filter(user=user)
                .filter(Q(status="success") | Q(status="failed"))
                .values_list("quest__slug", flat=True)
            )

        return context
