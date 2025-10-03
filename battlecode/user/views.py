from django.shortcuts import render

from battlecode.pagedata import PageData


current_page = "user"


def user_profile(request, username: str):
    pd = PageData(
        title=f"User {username}",
        description="Track your progress and available quests on your personal dashboard.",
        curr_page=current_page,
    )
    return render(request, "user_profile.html", context={"pd": pd})
