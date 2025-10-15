from datetime import timedelta

from django.http import HttpRequest
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from battlecode.pagedata import PageData
from battlecode.quest_settings import break_delta

from quests.models import Quest
from peer_review.models import Assignment


curr_page = "quests"


class QuestsAllView(ListView, LoginRequiredMixin):
    model = Quest
    template_name = "quests_all.html"
    context_object_name = "quests"

    paginate_by = 12

    def get_queryset(self):
        return Quest.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pd"] = PageData(
            title="Quests",
            description="Track your progress and available quests on your personal dashboard.",
            curr_page=curr_page,
        )

        context["accepted"] = Assignment.objects.filter(user=self.request.user, status="active").all()
        context["accepted_list"] = [item.quest.slug for item in context["accepted"]]

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
