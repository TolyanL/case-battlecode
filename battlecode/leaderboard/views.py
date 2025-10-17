from django.shortcuts import render
from django.http import HttpRequest
from django.db.models import Count

from battlecode.pagedata import PageData
from user.models import Profile


current_page = "leaderboard"


def leaderboard(request: HttpRequest):
    context = {}
    user = request.user

    context["pd"] = PageData(
        title="Leaderboard",
        description="Track your progress and available quests on your personal dashboard.",
        curr_page=current_page,
    )

    top_profiles = Profile.objects.filter(user__is_active=True).order_by("-pts")[:10]
    leaderboard_list = []

    user_in_leaderboard = None
    user_rank = None

    for rank, profile in enumerate(top_profiles, start=1):
        leaderboard_list.append({"rank": rank, "profile": profile})
        if user.is_authenticated and profile.user == user:
            user_in_leaderboard = {"rank": rank, "profile": profile}
    if user.is_authenticated and user_in_leaderboard is None:
        if hasattr(user, "profile"):
            user_pts = user.profile.pts
            user_rank = (
                Profile.objects.filter(user__is_active=True, pts__gt=user_pts).count()
                + 1
            )
            user_in_leaderboard = {"rank": user_rank, "profile": user.profile}

    context["leaderboard"] = leaderboard_list
    context["current_user_entry"] = user_in_leaderboard

    return render(request, "leaderboard.html", context)
