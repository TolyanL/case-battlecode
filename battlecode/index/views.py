from django.shortcuts import render

from battlecode.pagedata import PageData

from quests.models import Quest
from user.models import Profile

current_page = "index"


def index(request):
    pd = PageData(
        title="BattleCode — Learn by Doing",
        description="BattleCode — образовательная игровая платформа для программистов.",
        curr_page=current_page,
    )

    featured_quests = Quest.objects.filter(active=True).order_by("-created_at")[:4]

    context = {
        "pd": pd,
        "featured_quests": featured_quests,
    }

    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            context["profile"] = profile
            enrolled_courses = profile.courses.all()
            context["enrolled_courses"] = enrolled_courses
        except Profile.DoesNotExist:
            pass

    return render(request, "index.html", context)

