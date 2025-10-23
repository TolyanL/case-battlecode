# battlecode/courses/views.py
from django.views.generic import ListView, DetailView
from django.db.models import Q
from battlecode.pagedata import PageData
from user.models import Profile
from quests.models import Quest
from peer_review.models import Assignment
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
        user = self.request.user
        course = self.object

        # Проверяем, записан ли пользователь
        is_enrolled = Profile.objects.filter(user=user, courses=course).exists()
        context["accepted"] = is_enrolled

        # Проверяем, завершён ли курс
        course_completed = False
        if is_enrolled:
            # Все квесты курса
            course_quests = course.quests.all()
            total_quests = course_quests.count()

            if total_quests > 0:
                # Количество квестов с успешным статусом
                success_count = Assignment.objects.filter(
                    user=user,
                    quest__in=course_quests,
                    status="success"
                ).count()

                course_completed = (success_count == total_quests)

        context["course_completed"] = course_completed
        return context