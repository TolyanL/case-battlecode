from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from badges.manager import BadgeManager
from battlecode.pagedata import PageData
from user.models import Profile


current_page = "user"


@login_required
def user_profile(request, username: str):
    pd = PageData(
        title=f"User {username}",
        description="Track your progress and available quests on your personal dashboard.",
        curr_page=current_page,
    )
    profile = Profile.objects.get(user=request.user)

    BadgeManager(request.user).check_all_badges()

    return render(
        request,
        "user_profile.html",
        context={"pd": pd, "profile": profile},
    )
