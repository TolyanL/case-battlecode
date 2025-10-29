from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from battlecode.pagedata import PageData
from battlecode.quest_settings import break_delta
from battlecode.course_settings import break_delta as break_delta_c

from user.models import Profile
from peer_review.models import Assignment, CourseProgress
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
            u_profile, _ = Profile.objects.get_or_create(user=user)
            for c in courses:
                cp = (
                    CourseProgress.objects.filter(
                        user=user,
                        course=c,
                    )
                    .order_by("-completed_at")
                    .first()
                )
                c.progress = cp.progress_percent if cp else 0

                if u_profile.courses.filter(id=c.id).exists():
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


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = "course_detail.html"

    def get_object(self):
        c = super().get_object()

        ct = CourseProgress.objects.filter(
            user=self.request.user,
            course=c,
        ).first()

        c.progress = ct.progress_percent if ct else 0
        c.completed = ct.completed_at > break_delta_c() if ct and ct.completed_at else False

        return c

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["pd"] = PageData(
            title=f"Курс {self.object.title}",
            description="",
            curr_page=curr_page,
        )

        if user.is_authenticated:
            context["is_accepted"] = Profile.objects.filter(
                user=user,
                courses=self.object,
            ).exists()

            items = Assignment.objects.filter(user=user).filter(
                quest__courses=self.object, completed_at__gte=break_delta()
            )

            context["accepted"] = items.filter(status="active").values_list("quest__slug", flat=True)
            context["review"] = items.filter(status="completed").values_list("quest__slug", flat=True)
            context["success"] = items.filter(status="success").values_list("quest__slug", flat=True)
            context["failed"] = items.filter(status="failed").values_list("quest__slug", flat=True)

        return context
