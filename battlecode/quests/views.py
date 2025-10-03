from django.shortcuts import render

from battlecode.pagedata import PageData


current_page = "quests"


def quests_all(request):
    pd = PageData(
        title="Quests",
        description="Track your progress and available quests on your personal dashboard.",
        curr_page=current_page,
    )
    return render(request, "quests_all.html", context={"pd": pd})


def quests_check(request):
    pd = PageData(
        title="Quests",
        description="Track your progress and available quests on your personal dashboard.",
        curr_page=current_page,
    )
    return render(request, "quests_check.html", context={"pd": pd})
