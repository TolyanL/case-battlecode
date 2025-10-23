from django.http import HttpRequest
from django.shortcuts import render

from django.db.models import Q, Avg, Count

from battlecode.pagedata import PageData

from user.models import Profile
from quests.models import Language
from peer_review.models import Assignment


curr_page = "leaderboard"


def leaderboard(request: HttpRequest):
    leaderboard_list, curr_user_entry = get_leaderboard_data(request.user)
    side = side_data()

    context = {
        "pd": PageData(
            curr_page=curr_page,
            title="Leaderboard",
            description="Track your progress and available quests on your personal dashboard.",
        ),
        "leaderboard": leaderboard_list,
        "side_data": side,
        "current_user_entry": curr_user_entry,
    }

    return render(request, "leaderboard.html", context)


def side_data() -> dict:
    data = {}

    data["total_players"] = Profile.objects.filter(
        user__is_active=True,
        user__is_staff=False,
    ).count()

    data["total_matches"] = Assignment.objects.filter(
        Q(status="success") | Q(status="failed"),
    ).count()

    avg_pts = Assignment.objects.filter(
        Q(status="success") | Q(status="failed"),
    ).aggregate(avg_given_pts=Avg("given_pts"))["avg_given_pts"]
    data["average_pts"] = avg_pts if avg_pts else 0

    data["popular_language"] = (
        Language.objects.filter(quests__assignments__isnull=False)
        .annotate(total_assignments=Count("quests__assignments"))
        .order_by("-total_assignments")
        .first()
    )

    return data


def get_leaderboard_data(user) -> tuple[list, dict]:
    top_profiles = Profile.objects.filter(user__is_active=True).order_by("-pts")[:10]

    leaderboard_list = []
    current_user_entry = None

    for rank, profile in enumerate(top_profiles, start=1):
        success_count = Assignment.objects.filter(
            Q(status="success") | Q(status="failed"),
            user=profile.user,
        ).count()

        entry = {
            "rank": rank,
            "profile": profile,
            "matches": success_count,
        }
        leaderboard_list.append(entry)

        if user.is_authenticated and profile.user == user:
            current_user_entry = entry

    if user.is_authenticated and not current_user_entry:
        curr_user_profile = Profile.objects.filter(user=user).first()
        if not curr_user_profile:
            curr_user_profile = Profile.objects.create(user=user)

        user_pts = curr_user_profile.pts

        user_rank = Profile.objects.filter(user__is_active=True, pts__gt=user_pts).count() + 1

        success_count = Assignment.objects.filter(
            user=user,
            status="success",
        ).count()

        current_user_entry = {
            "rank": user_rank,
            "profile": curr_user_profile,
            "success_assignments": success_count,
        }

    return leaderboard_list, current_user_entry
