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

    assignments = Assignment.objects.filter(user=user).order_by("-assigned_at").all()

    # Передаём max_reviews (замените на реальное значение, если оно динамическое)
    MAX_REVIEWS = 3  # ← настройте под ваш проект

    recent_activities = get_recent_activity(user.id, assignments, MAX_REVIEWS)
    all_langs, top_langs = get_pref_langs_data(assignments, top_n=10)

    pd = PageData(
        title=f"Профиль — {user.username}",
        description=f"Страница профиля пользователя {user.username}.",
        curr_page="user",
        max_reviews=MAX_REVIEWS,
    )

    return render(
        request,
        "user_profile.html",
        context={
            "pd": pd,
            "user": user,  # важно: в шаблоне используется {{ user }}
            "profile": profile,
            "assignments": assignments,
            "recent_activities": recent_activities,
            "preferred_languages_chart": all_langs,
            "preferred_languages_text": top_langs,
        },
    )


def get_recent_activity(user_id: int, assignments: list[Assignment], max_reviews: int) -> list:
    DIFFICULTY_COLORS = {
        "easy": {"bg": "bg-green-500/20", "text": "text-green-500"},
        "medium": {"bg": "bg-orange-500/20", "text": "text-orange-500"},
        "hard": {"bg": "bg-red-500/20", "text": "text-red-500"},
        "default": {"bg": "bg-gray-500", "text": "text-white"},
    }

    recent_activities = []

    for assignment in assignments:
        difficulty = assignment.quest.difficulty
        assignment.difficulty_color = DIFFICULTY_COLORS.get(difficulty, DIFFICULTY_COLORS["default"])
        assignment.max_reviews = max_reviews  # ← передаём в шаблон
        recent_activities.append({"object": assignment, "type": "assignment", "date": assignment.updated_at})

    reviews = Review.objects.filter(user__id=user_id).order_by("-created_at").all()
    for review in reviews:
        recent_activities.append({"object": review, "type": "review", "date": review.created_at})

    recent_activities.sort(key=lambda x: x["date"], reverse=True)
    return recent_activities[:5]


def get_pref_langs_data(assignments: list[Assignment], top_n: int = 10):
    lang_counts = {}

    for assignment in assignments:
        if assignment.status == "active":
            continue
        lang = assignment.quest.language
        lang_counts[lang.name] = lang_counts.get(lang.name, 0) + 1

    total = sum(lang_counts.values())
    if total == 0:
        return [], []

    lang_list = []
    for name, count in lang_counts.items():
        color = None
        for a in assignments:
            if a.status != "active" and a.quest.language.name == name:
                color = a.quest.language.color
                break
        percentage = (count / total) * 100
        lang_list.append({
            "name": name,
            "color": color or "#666666",
            "percentage": percentage,
            "count": count,
        })

    lang_list.sort(key=lambda x: x["percentage"], reverse=True)

    # Топ-N для текста
    top_langs = [
        {**lang, "percentage": round(lang["percentage"])}
        for lang in lang_list[:top_n]
    ]

    # Все языки для диаграммы
    total_pct = 0.0
    chart_langs = []
    n = len(lang_list)
    for i, lang in enumerate(lang_list):
        pct = lang["percentage"]
        if i == n - 1:
            dash_length = max(0.0, 100.0 - total_pct)
        else:
            dash_length = pct

        if dash_length < 0.5:
            dash_length = 0.5
            total_pct = 100.0

        chart_langs.append({
            "name": lang["name"],
            "color": lang["color"],
            "percentage": round(lang["percentage"]),
            "dash_array_length": dash_length,
            "dash_array_gap": 100.0 - dash_length,
            "dash_offset": -total_pct,
        })
        total_pct += dash_length

    return chart_langs, top_langs