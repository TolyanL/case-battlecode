from django.shortcuts import render

from battlecode.pagedata import PageData

current_page = "quests"


def all_quests(request):
    pd = PageData(
        title="Quests",
        description="Track your progress and available quests on your personal dashboard.",
        curr_page=current_page,
    )
    return render(request, "all_quests.html", context={"pd": pd})
