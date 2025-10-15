from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from battlecode.pagedata import PageData
from badges.manager import BadgeManager

from user.models import Profile
from peer_review.models import Assignment, Review


current_page = "user"


@login_required
def user_profile(request, username: str):
    if username == "me":
        user = request.user
    else:
        user = get_object_or_404(User, username=username)

    profile = getattr(user, "profile", None)
    if not profile:
        profile = Profile.objects.create(user=user)

    BadgeManager(user).check_all_badges()

    assignments = Assignment.objects.filter(user=user).order_by("-assigned_at")[:5]

    recent_activities = get_recent_activity(user.id, assignments)
    preferred_languages = get_pref_langs(assignments)

    pd = PageData(
        title=f"Профиль — {user.username}",
        description=f"Страница профиля пользователя {user.username}.",
        curr_page="user",
    )

    return render(
        request,
        "user_profile.html",
        context={
            "pd": pd,
            "profile_user": user,
            "profile": profile,
            "assignments": assignments,
            "recent_activities": recent_activities,
            "preferred_languages": preferred_languages,
        },
    )


def get_recent_activity(user_id: int, assignments: list[Assignment]) -> list[Assignment]:
    DIFFICULTY_COLORS = {
        "easy": {"bg": "bg-green-500/20", "text": "text-green-500"},
        "medium": {"bg": "bg-orange-500/20", "text": "text-orange-500"},
        "hard": {"bg": "bg-red-500/20", "text": "text-red-500"},
        "default": {"bg": "bg-gray-500", "text": "text-white"},
    }

    for assignment in assignments:
        difficulty = assignment.quest.difficulty
        assignment.difficulty_color = DIFFICULTY_COLORS.get(difficulty, DIFFICULTY_COLORS["default"])

    recent_activities = []

    for activity in assignments:
        difficulty = activity.quest.difficulty
        activity.difficulty_color = DIFFICULTY_COLORS.get(difficulty, DIFFICULTY_COLORS["default"])
        recent_activities.append({"object": activity, "type": "assignment", "date": activity.assigned_at})

    reviews = Review.objects.filter(user__id=user_id).order_by("-created_at")
    for review in reviews:
        recent_activities.append({"object": review, "type": "review", "date": review.created_at})

    recent_activities = sorted(recent_activities, key=lambda x: x["date"], reverse=True)

    return recent_activities


def get_pref_langs(assignments: list[Assignment]) -> list[dict]:
    lang_counts = {}
    pref_langs = []

    for assignment in assignments:
        lang = assignment.quest.language
        if lang.name in lang_counts:
            lang_counts[lang.name][0] += 1
        else:
            lang_counts[lang.name] = [1, lang.color]

    total_assignments = sum(i[0] for i in lang_counts.values())

    if total_assignments > 0:
        total_percentage = 0
        for lang_name, (count, color) in lang_counts.items():
            percentage = int((count / total_assignments) * 100)

            start_angle = total_percentage * 360 / 100
            total_percentage += percentage
            end_angle = total_percentage * 360 / 100

            dash_array_length = percentage

            dash_array_gap = 100 - percentage

            dash_offset = -(start_angle / 360) * 100
            pref_langs.append(
                {
                    "name": lang_name,
                    "color": color,
                    "percentage": percentage,
                    "count": count,
                    "start_angle": start_angle,
                    "end_angle": end_angle,
                    "dash_array_length": dash_array_length,
                    "dash_array_gap": dash_array_gap,
                    "dash_offset": dash_offset,
                }
            )

    pref_langs.sort(key=lambda x: x["percentage"], reverse=True)
    return pref_langs
