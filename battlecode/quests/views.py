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
