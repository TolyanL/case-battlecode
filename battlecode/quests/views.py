from datetime import timedelta

from django.http import HttpRequest, HttpResponse
from django.db.models import Q
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from battlecode.pagedata import PageData
from battlecode.quest_settings import break_delta

from quests.models import Quest
from peer_review.models import Assignment


curr_page = "quests"


@login_required
def quests_all(request: HttpRequest) -> HttpResponse:
    pd = PageData(
        title="Quests",
        description="Track your progress and available quests on your personal dashboard.",
        curr_page=curr_page,
    )
    quests = Quest.objects.filter(active=True).all()

    accepted = Assignment.objects.filter(user=request.user, status="active").all()
    accepted_list = [item.quest.slug for item in accepted]

    return render(
        request,
        "quests_all.html",
        context={
            "pd": pd,
            "quests": quests,
            "accepted": accepted,
            "accepted_list": accepted_list,
        },
    )


class QuestDetailView(DetailView, LoginRequiredMixin):
    model = Quest
    template_name = "quest_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pd"] = PageData(
            title="Quest Detail",
            description="Details about the selected quest.",
            curr_page=curr_page,
        )

        accepted = Assignment.objects.filter(user=self.request.user, status="active").all()
        context["accepted_list"] = [item.quest.slug for item in accepted]

        completed = (
            Assignment.objects.filter(
                user=self.request.user,
                completed_at__isnull=False,
                completed_at__gte=break_delta(),
            )
            .filter(Q(status="completed") | Q(status="failed"))
            .all()
        )
        context["completed_list"] = [item.quest.slug for item in completed]

        context["failed"] = (
            Assignment.objects.filter(user=self.request.user)
            .filter(status="failed", completed_at__gte=break_delta())
            .exists()
        )

        return context


class QuestWorkView(DetailView, LoginRequiredMixin):
    model = Quest
    template_name = "quest_work.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pd"] = PageData(
            title="Quest Detail",
            description="Details about the selected quest.",
            curr_page=curr_page,
        )
        context["work_timer"] = timedelta(hours=self.object.work_time)

        accepted = Assignment.objects.filter(user=self.request.user, status="active").all()
        context["accepted_list"] = [item.quest.slug for item in accepted]

        completed = (
            Assignment.objects.filter(user=self.request.user)
            .filter(
                Q(status="completed") | Q(status="failed"),
                Q(completed_at__gte=break_delta()),
            )
            .all()
        )
        context["completed_list"] = [item.quest.slug for item in completed]

        return context

    def get(self, request, *args, **kwargs):
        if (
            Assignment.objects.filter(user=self.request.user)
            .filter(status="failed", completed_at__gte=break_delta())
            .exists()
        ):
            return redirect("quests_all")
        return super().get(request, *args, **kwargs)


def quest_reviews(request: HttpRequest, slug: str):
    quest = get_object_or_404(Quest, slug=slug, active=True)

    if not Assignment.objects.filter(
        user=request.user,
        quest=quest,
        status="completed",
    ).exists():
        return redirect("quest_detail", slug=slug)

    context = {}
    context["pd"] = PageData(
        title=f"Проверка: {quest.title}",
        description="Список работ участников для оценки.",
        curr_page=curr_page,
    )
    context["quest"] = quest
    context["items"] = Assignment.objects.filter(quest=quest, status="completed").order_by("-completed_at").all()

    return render(request, "quest_reviews.html", context)


# @login_required
# def courses_all(request: HttpRequest) -> HttpResponse:
#     """
#     Отображает список всех активных курсов.
#     """
#     pd = PageData(
#         title="Courses",
#         description="Browse and enroll in courses to develop your skills.",
#         curr_page=current_page_courses,  # Используем новое значение
#     )
#     courses = (
#         Course.objects.filter(active=True).prefetch_related("skills", "quests").all()
#     )  # Используем ManyToManyField 'quests'
#     enrolled_courses = request.user.profile.enrolled_courses.all()  # Получаем из профиля
#     enrolled_slugs = {course.slug for course in enrolled_courses}
#     # print(f"DEBUG: Enrolled slugs for {request.user}: {enrolled_slugs}") # Отладка
#
#     return render(
#         request,
#         "courses_all.html",  # Новый шаблон
#         context={
#             "pd": pd,
#             "courses": courses,
#             "enrolled_slugs": enrolled_slugs,
#             "max_courses": 3,  # Передаём лимит
#         },
#     )
#
#
# class CourseDetailView(DetailView, LoginRequiredMixin):
#     model = Course
#     template_name = "course_detail.html"  # Новый шаблон
#     slug_field = "slug"  # Указываем поле для поиска
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["pd"] = PageData(
#             title="Course Detail",
#             description=f"Details about the selected course: {self.object.title}.",
#             curr_page=current_page_courses,  # Используем новое значение
#         )
#         # --- ИЗМЕНЕНО: Используем ManyToManyField для получения квестов ---
#         context["course_quests"] = self.object.quests.filter(active=True).all()  # <-- ПРАВИЛЬНО
#
#         enrolled_courses = self.request.user.profile.enrolled_courses.all()
#         context["enrolled_slugs"] = {course.slug for course in enrolled_courses}
#         context["max_courses"] = 3  # Передаём лимит
#         return context
#
#
# # Представление для записи на курс
# @login_required
# def enroll_course(request: HttpRequest) -> HttpResponse:
#     if request.method == "POST":
#         course_slug = request.POST.get("course_slug")
#         course = get_object_or_404(Course, slug=course_slug, active=True)
#
#         profile = request.user.profile
#         if profile.enrolled_courses.count() >= 3:
#             # TODO: Добавить сообщение об ошибке (messages framework)
#             print(f"User {request.user} already enrolled in 3 courses.")
#             return redirect("courses_all")
#
#         profile.enrolled_courses.add(course)
#         # TODO: Добавить сообщение об успехе (messages framework)
#         print(f"User {request.user} enrolled in course {course.title}.")
#     return redirect("courses_all")  # Возврат на страницу курсов
#
#
# # Представление для отписки от курса
# @login_required
# def unenroll_course(request: HttpRequest) -> HttpResponse:
#     if request.method == "POST":
#         course_slug = request.POST.get("course_slug")
#         course = get_object_or_404(Course, slug=course_slug)
#
#         profile = request.user.profile
#         profile.enrolled_courses.remove(course)
#         # TODO: Добавить сообщение об успехе (messages framework)
#         print(f"User {request.user} unenrolled from course {course.title}.")
#     return redirect("courses_all")  # Возврат на страницу курсов
#
#
# # --- /НОВЫЕ ПРЕДСТАВЛЕНИЯ ДЛЯ КУРСОВ ---
