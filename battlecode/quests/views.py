from django.shortcuts import render
from django.views.generic import DetailView

from battlecode.pagedata import PageData

from quests.models import Quest, Assignment


current_page = "quests"


def quests_all(request):
    pd = PageData(
        title="Quests",
        description="Track your progress and available quests on your personal dashboard.",
        curr_page=current_page,
    )

    quests = Quest.objects.filter(active=True)
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
        accepted = Assignment.objects.filter(user=self.request.user, status="active").all()
        context["accepted_list"] = [item.quest.slug for item in accepted]
        return context


def quests_check(request):
    pd = PageData(
        title="Quests",
        description="Track your progress and available quests on your personal dashboard.",
        curr_page=current_page,
    )
    return render(request, "quests_check.html", context={"pd": pd})
