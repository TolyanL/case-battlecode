from django.shortcuts import render
from django.views.generic import DetailView

from battlecode.pagedata import PageData

from .models import Quest


current_page = "quests"


def quests_all(request):
    pd = PageData(
        title="Quests",
        description="Track your progress and available quests on your personal dashboard.",
        curr_page=current_page,
    )
    quests = Quest.objects.filter(active=True)
    return render(request, "quests_all.html", context={"pd": pd, "quests": quests})


class QuestDetailView(DetailView):
    model = Quest
    template_name = "quest_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pd"] = PageData(
            title="Quest Detail",
            description="Details about the selected quest.",
            curr_page=current_page,
        )
        return context


def quests_check(request):
    pd = PageData(
        title="Quests",
        description="Track your progress and available quests on your personal dashboard.",
        curr_page=current_page,
    )
    return render(request, "quests_check.html", context={"pd": pd})
