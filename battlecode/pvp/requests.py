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

            item, created = PvpAssignment.objects.get_or_create(
                user=opp,
                opponent=user,
                battle=battle,
                status="active",
            )

            url = battle.get_absolute_url()

            return JsonResponse({"success": True, "message": url})
        except Exception as e:
            logger.error(e)
            return JsonResponse({"success": False, "message": "Error has occurred"})

    return JsonResponse({"success": False, "message": "Empty request"})


@login_required
def change_state(request: HttpRequest):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            username = data.get("user")
            state = data.get("state")

            if not username or not state:
                return JsonResponse({"success": False, "message": ""})

            item = PvpAssignment.objects.filter(user__username=username, status="active").first()
            if state == "ready":
                item.is_ready = True
            if state == "not-ready":
                item.is_ready = False
            item.save()

            battle = item.battle.pvp_assignments.all()
            if all([i.is_ready for i in battle]):
                item.battle.start()
                return JsonResponse({"success": True, "message": f"{item.battle.code}/do"})

            return JsonResponse({"success": True, "message": ""})

        except Exception as e:
            logger.error(e)
            return JsonResponse({"success": False, "message": ""})

    return JsonResponse({"success": False, "message": "Empty request"})


@login_required
def skip(request: HttpRequest):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            username = data.get("user")
            if not username:
                return JsonResponse({"success": False, "message": "Empty request"})

            item = PvpAssignment.objects.filter(user__username=username, status="active").first()
            item.skip()

            return JsonResponse({"success": True, "message": "Battle changed"})

        except Exception as e:
            logger.error(e)
            return JsonResponse({"success": False, "message": "Error has occurred"})

    return JsonResponse({"success": False, "message": "Empty request"})


@login_required
def fail(request: HttpRequest):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            username = data.get("user")
            if not username:
                return JsonResponse({"success": False, "message": "Empty request"})

            item = PvpAssignment.objects.filter(user__username=username, status="active").first()
            item.fail(request.user.id)

            return JsonResponse({"success": True, "message": "Battle changed"})

        except Exception as e:
            logger.error(e)
            return JsonResponse({"success": False, "message": "Error has occurred"})

    return JsonResponse({"success": False, "message": "Empty request"})


@login_required
def complete(request: HttpRequest):
    if request.method == "POST":
        user = request.user
        try:
            data = json.loads(request.body)

            completed = data.get("action")
            code = data.get("code")
            if not code or not completed:
                return JsonResponse({"success": False, "message": "Empty request"})

            item = PvpAssignment.objects.filter(user=user, battle__code=code, status="active").first()
            if not item:
                return JsonResponse({"success": False, "message": "Battle not found"})

            item.complete()

            return JsonResponse({"success": True, "message": "Battle changed"})

        except Exception as e:
            logger.error(e)
            return JsonResponse({"success": False, "message": "Error has occurred"})

    return JsonResponse({"success": False, "message": "Empty request"})
