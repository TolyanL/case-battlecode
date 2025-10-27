from django.http import HttpRequest
from django.shortcuts import render

from django.db.models import Q, Avg, Count
from django.contrib.auth.models import Group

from battlecode.pagedata import PageData
from battlecode.groups import STUDENT_GROUP

from user.models import Profile
from quests.models import Language
from peer_review.models import Assignment


curr_page = "leaderboard"


def leaderboard(request: HttpRequest):
    leaderboard_list, curr_user_entry = get_leaderboard_data(request.user)
    side = side_data()

    context = {
        "pd": PageData(
            curr_page="leaderboard",
            title="Leaderboard",
            description="Track your progress and available quests on your personal dashboard.",
        ),
        "leaderboard": leaderboard_list,
        "side_data": side,
        "current_user_entry": curr_user_entry,
    }

    return render(request, "leaderboard.html", context)


def side_data() -> dict:
    student_group = Group.objects.filter(name=STUDENT_GROUP).first()
    if not student_group:
        return {
            "total_players": 0,
            "total_matches": 0,
            "average_pts": 0,
            "popular_language": None,
        }

    student_users = student_group.user_set.filter(
        is_active=True,
        is_staff=False,
    )

    data = {}

    data["total_players"] = student_users.count()

    data["total_matches"] = Assignment.objects.filter(
        Q(status="success") | Q(status="failed"),
        user__in=student_users,
    ).count()

    avg_pts = Assignment.objects.filter(
        Q(status="success") | Q(status="failed"),
        user__in=student_users,
    ).aggregate(avg_given_pts=Avg("given_pts"))["avg_given_pts"]
    data["average_pts"] = avg_pts if avg_pts is not None else 0

    data["popular_language"] = (
        Language.objects.filter(
            quests__assignments__user__in=student_users, quests__assignments__status__in=["success", "failed"]
        )
        .annotate(total_assignments=Count("quests__assignments"))
        .order_by("-total_assignments")
        .first()
    )

    return data


def get_leaderboard_data(curr_user) -> tuple[list, dict]:
    student_group = Group.objects.filter(name=STUDENT_GROUP).first()
    if not student_group:
        return [], None

    student_users = student_group.user_set.filter(
        is_active=True,
        is_staff=False,
        is_superuser=False,
    )

    top_profiles = Profile.objects.filter(
        user__in=student_users,
    ).order_by("-pts")[:10]

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

        if curr_user.is_authenticated and profile.user == curr_user:
            current_user_entry = entry

    if curr_user.is_authenticated and not current_user_entry:
        if curr_user in student_users:
            curr_user_profile = Profile.objects.filter(user=curr_user).first()
            if not curr_user_profile:
                curr_user_profile = Profile.objects.create(user=curr_user)

            user_pts = curr_user_profile.pts

            user_rank = Profile.objects.filter(user__in=student_users, pts__gt=user_pts).count() + 1

            success_count = Assignment.objects.filter(
                Q(status="success") | Q(status="failed"),
                user=curr_user,
            ).count()

            current_user_entry = {
                "rank": user_rank,
                "profile": curr_user_profile,
                "success_assignments": success_count,
            }

    return leaderboard_list, current_user_entry
