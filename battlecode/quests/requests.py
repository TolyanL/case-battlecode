import json
from datetime import datetime

from django.http import HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required

from battlecode.quest_settings import MAX_PICKED_QUESTS

from user.models import Profile
from quests.models import Quest
from peer_review.models import Assignment


@login_required()
def accept_quest(request: HttpRequest):
    if request.method == "POST":
        user = request.user
        try:
            data = json.loads(request.body)

            quest_slug = data.get("quest_slug")
            if not quest_slug:
                return JsonResponse({"success": False, "message": "Empty request"})

            quest = Quest.objects.get(slug=quest_slug)
            if not quest:
                return JsonResponse({"success": False, "message": "Quest not found"})

            items = Assignment.objects.filter(user=user, quest=quest, status="active")
            if len(items) >= MAX_PICKED_QUESTS:
                return JsonResponse({"success": False, "message": "You already have the maximum number of quests"})
            if items.exists():
                return JsonResponse({"success": False, "message": "You already have an active quest"})

            Assignment.objects.create(user=user, quest=quest)

            return JsonResponse({"success": True, "message": "Quest accepted"})
        except Exception as e:
            print("err: ", e)
            return JsonResponse({"success": False, "message": "Error has occurred"})

    return JsonResponse({"success": False, "message": "Empty request"})


@login_required()
def give_up_quest(request: HttpRequest):
    if request.method == "POST":
        user = request.user
        try:
            data = json.loads(request.body)

            quest_slug = data.get("quest_slug")
            if not quest_slug:
                return JsonResponse({"success": False, "message": "Empty request"})

            quest = Quest.objects.get(slug=quest_slug)
            if not quest:
                return JsonResponse({"success": False, "message": "Quest not found"})

            items = Assignment.objects.filter(user=user, quest=quest, status="active")
            if not items.exists():
                return JsonResponse({"success": False, "message": "You have no active quests"})

            Assignment.objects.filter(user=user, quest=quest, status="active").update(
                status="failed",
                given_pts=-quest.penalty,
                completed_at=datetime.now(),
            )
            if quest.penalty > 0:
                profile = Profile.objects.get(user=user)
                profile.pts -= quest.penalty
                profile.save()

            return JsonResponse({"success": True, "message": "Quest failed"})
        except Exception as e:
            print("err: ", e)
            return JsonResponse({"success": False, "message": "Error has occurred"})

    return JsonResponse({"success": False, "message": "Empty request"})


@login_required
def complete_quest(request: HttpRequest):
    if request.method == "POST":
        user = request.user
        try:
            data = json.loads(request.body)

            quest_slug = data.get("quest_slug")
            if not quest_slug:
                return JsonResponse({"success": False, "message": "Empty request"})

            quest = Quest.objects.get(slug=quest_slug)
            if not quest:
                return JsonResponse({"success": False, "message": "Quest not found"})

            items = Assignment.objects.filter(user=user, quest=quest, status="active")
            if not items.exists():
                return JsonResponse({"success": False, "message": "You have no active quests"})

            code = data.get("data") or ""

            Assignment.objects.filter(user=user, quest=quest, status="active").update(
                status="completed",
                completed_at=datetime.now(),
                code=code,
            )

            return JsonResponse({"success": True, "message": "Quest completed"})
        except Exception as e:
            print("err: ", e)
            return JsonResponse({"success": False, "message": "Error has occurred"})

    return JsonResponse({"success": False, "message": "Empty request"})
