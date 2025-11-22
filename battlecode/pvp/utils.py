from random import choice

from django.utils import timezone
from django.contrib.auth.models import User

from user.models import Profile

from battlecode.redis_settings import client
from battlecode.pvp_settings import REDIS_TTL, LEVEL_DELTA


def last_users() -> list[User]:
    last_users = []
    now = timezone.now() - timezone.timedelta(minutes=REDIS_TTL / 60)

    for u in User.objects.filter().all():
        val = client.get(f"user-last-active-{u.id}")
        if not val:
            continue

        last_login = float()
        if last_login > now.timestamp():
            last_users.append(u)

    return last_users


def get_opponent(curr_user: User, users: list[User]) -> User | None:
    fits = []

    for u in users:
        # WARN: uncomment this line in final version
        # if u.id == curr_user.id:
        #     continue

        curr_p = Profile.objects.get(user=curr_user)
        p = Profile.objects.get(user=u)

        if p.pts - LEVEL_DELTA <= curr_p.pts <= p.pts + LEVEL_DELTA:
            fits.append(u)

    if not fits:
        return None

    return choice(fits)
