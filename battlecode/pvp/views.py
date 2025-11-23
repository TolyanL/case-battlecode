from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from pvp.models import PvpAssignment, Battle

from user.models import Profile
from battlecode.pagedata import PageData

from pvp.utils import last_users, get_opponent


curr_page = "pvp"


@login_required
def dashboard(request: HttpRequest):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    lasts = last_users()
    opp = get_opponent(user, lasts)

    curr_battle = PvpAssignment.objects.filter(user=user, status="active").first()

    pd = PageData(
        "PvP Dashboard",
        "PvP",
        curr_page,
    )

    return render(
        request,
        "start.html",
        {
            "pd": pd,
            "profile": profile,
            "opponents": len(lasts),
            "opponent": opp,
            "curr_battle": curr_battle,
        },
    )


@login_required
def battle(request: HttpRequest, code: str):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    item = PvpAssignment.objects.filter(user=user, battle__code=code).first()
    if not item:
        return redirect("pvp_dashboard")

    if item.created_at < timezone.now() - timezone.timedelta(minutes=10):
        item.skip()
        return redirect("pvp_dashboard")

    pd = PageData(
        "PVP Battle",
        "PVP",
        "pvp",
    )

    return render(
        request,
        "wait_ready.html",
        {
            "pd": pd,
            "item": item,
            "profile": profile,
            "opponent": item.opponent,
        },
    )


@login_required
def do_task(request: HttpRequest, code: str):
    user = request.user

    item = PvpAssignment.objects.filter(user=user, battle__code=code).first()
    print(item)
    if not item:
        print("Not found")
        return redirect("pvp_dashboard")

    pd = PageData(
        "PVP Battle",
        "PVP",
        "pvp",
    )

    return render(
        request,
        "pvp_work.html",
        {
            "pd": pd,
            "quest": item.battle.quest,
        },
    )
