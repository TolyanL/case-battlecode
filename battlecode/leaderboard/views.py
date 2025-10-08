from django.shortcuts import render

from battlecode.pagedata import PageData

current_page = "leaderboard"


def leaderboard(request):
    pd = PageData(
        title="Leaderboard",
        description="Track your progress and available quests on your personal dashboard.",
        curr_page=current_page,
    )
    return render(request, "leaderboard.html", context={"pd": pd})
