import json

from random import choice

from django.http import HttpRequest, JsonResponse
from django.contrib.auth.forms import User
from django.contrib.auth.decorators import login_required

from pvp.models import PvpAssignment, Battle
from quests.models import Quest

from logging import getLogger


logger = getLogger(__name__)


@login_required
def start_battle(request: HttpRequest):
    if request.method == "POST":
        user = request.user
        try:
            data = json.loads(request.body)

            opponent = data.get("opponent")
            if not opponent:
                return JsonResponse({"success": False, "message": "Empty request"})

            opp = User.objects.get(username=opponent)

            quests = Quest.objects.filter(task_type="pvp").all()
            if not len(quests):
                return JsonResponse({"success": False, "message": "No PvP quests found"})

            quest = choice(quests)
            battle = Battle.objects.create(quest=quest)

            item, created = PvpAssignment.objects.get_or_create(
                user=user,
                opponent=opp,
                battle=battle,
                status="active",
            )
            if not created:
                return JsonResponse({"success": False, "message": "You have an active battle"})

            url = battle.get_absolute_url()

            return JsonResponse({"success": True, "message": url})
        except Exception as e:
            logger.error(e)
            return JsonResponse({"success": False, "message": "Error has occurred"})

    return JsonResponse({"success": False, "message": "Empty request"})


@login_required
def ready(request: HttpRequest):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            username = data.get("user")
            state = data.get("state")

            if not username or not state:
                return JsonResponse({"success": False, "message": "Empty request"})

            item = PvpAssignment.objects.filter(user__username=username, status="active").first()
            if state == "ready":
                item.is_ready = True
            if state == "not-ready":
                item.is_ready = False
            item.save()

            return JsonResponse({"success": True, "message": "Battle changed"})

        except Exception as e:
            logger.error(e)
            return JsonResponse({"success": False, "message": "Error has occurred"})

    return JsonResponse({"success": False, "message": "Empty request"})
