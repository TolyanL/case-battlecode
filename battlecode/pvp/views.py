from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from pvp.models import PvpAssignment

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
        },
    )


@login_required
def battle(request: HttpRequest):
    user = request.user

    if PvpAssignment.objects.filter(user=user).exists():
        return redirect("pvp_dashboard")
