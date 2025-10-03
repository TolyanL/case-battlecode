from django.shortcuts import render

from battlecode.pagedata import PageData

current_page = "dashboard"


def dashboard(request):
    pd = PageData(
        title="Quest Dashboard",
        description="Track your progress and available quests on your personal dashboard.",
        curr_page=current_page,
    )
    return render(request, "dashboard.html", context={"pd": pd})
