from datetime import timedelta

from django.http import HttpRequest
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from battlecode.pagedata import PageData
from battlecode.quest_settings import break_delta

from user.models import Profile
from quests.models import Quest
from courses.models import Course
from peer_review.models import Assignment


curr_page = "quests"


class QuestsAllView(ListView, LoginRequiredMixin):
    model = Quest
    template_name = "quests_all.html"
    context_object_name = "quests"

    paginate_by = 12

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return ()

        quests = Quest.objects.filter(
            course_quests__course__enrolled_profiles__user=user,
        ).distinct()
        return quests

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pd"] = PageData(
            title="Quests",
            description="Track your progress and available quests on your personal dashboard.",
            curr_page=curr_page,
        )

        user = self.request.user

        if self.request.user.is_authenticated:
            context["accepted"] = [
                i.quest.slug for i in (Assignment.objects.filter(user=user).filter(status="active").all())
            ]
            context["review"] = [
                i.quest.slug for i in (Assignment.objects.filter(user=user).filter(status="completed").all())
            ]
            context["completed"] = [
                i.quest.slug
                for i in (
                    Assignment.objects.filter(user=user)
                    .filter(
                        Q(status="success") | Q(status="failed"),
                        Q(completed_at__gte=break_delta()),
                    )
                    .all()
                )
            ]
        context["courses"] = Course.objects.all()
        return context


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

        button_state = "start"  # 'start', 'continue_work', 'to_reviews', 'on_timeout'

        user = self.request.user
        quest = self.get_object()

        assignment = Assignment.objects.filter(user=user, quest=quest).order_by("-updated_at").first()

        if assignment:
            if assignment.status == "active":
                button_state = "continue_work"
            elif assignment.status == "completed":
                button_state = "to_reviews"
            elif assignment.status in ["success", "failed"]:
                if assignment.completed_at and assignment.completed_at > break_delta():
                    button_state = "on_timeout"

        context["button_state"] = button_state

        return context

    def get(self, request, *args, **kwargs):
        course = self.get_object().courses.first()
        if not Profile.objects.filter(user=self.request.user, courses=course).exists():
            return redirect("quests_all")
        return super().get(request, *args, **kwargs)


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

        context["completed"] = [
            item.quest.slug
            for item in (
                Assignment.objects.filter(user=self.request.user)
                .filter(
                    Q(status="success") | Q(status="failed"),
                )
                .filter(
                    quest__slug=self.kwargs["slug"],
                    completed_at__gte=break_delta(),
                )
                .all()
            )
        ]

        return context

    def get(self, request, *args, **kwargs):
        course = self.get_object().courses.first()
        if not Profile.objects.filter(user=self.request.user, courses=course).exists():
            return redirect("quests_all")

        if (
            Assignment.objects.filter(user=self.request.user)
            .filter(Q(status="success") | Q(status="failed"))
            .filter(
                quest__slug=self.kwargs["slug"],
                completed_at__gte=break_delta(),
            )
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
