from django.shortcuts import render
from django.http import HttpRequest
from django.db.models import Count
from battlecode.pagedata import PageData
from user.models import Profile
from peer_review.models import Assignment


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
        success_count = Assignment.objects.filter(
            user=profile.user,
            status="success",
        ).count()

        leaderboard_list.append(
            {
                "rank": rank,
                "profile": profile,
                "success_assignments": success_count,
            }
        )

        if user.is_authenticated and profile.user == user:
            user_in_leaderboard = {
                "rank": rank,
                "profile": profile,
                "success_assignments": success_count,
            }

    if user.is_authenticated and not user_in_leaderboard:
        current_user_profile = Profile.objects.get(user=user)
        user_pts = current_user_profile.pts

        user_rank = Profile.objects.filter(user__is_active=True, pts__gt=user_pts).count() + 1

        success_count = Assignment.objects.filter(
            user=user,
            status="success",
        ).count()

        user_in_leaderboard = {
            "rank": user_rank,
            "profile": current_user_profile,
            "success_assignments": success_count,
        }

    context["leaderboard"] = leaderboard_list
    context["current_user_entry"] = user_in_leaderboard

    return render(request, "leaderboard.html", context)