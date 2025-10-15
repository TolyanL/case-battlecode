from dataclasses import dataclass

from django.contrib.auth.forms import User

from battlecode.settings import REDIS_TTL

from peer_review.models import Assignment
from user.models import Profile

from badges import badges_checkers as checkers
from badges.models import Badge
from badges.redis import client


def _make_quest_property(status: str, redis_key: str):
    def getter(self):
        value = client.get(redis_key)

        if value is not None:
            return int(value)

        db_value = Assignment.objects.filter(user=self.user, status=status).count()
        client.setex(redis_key, REDIS_TTL, db_value)

        return db_value

    def setter(self, value: int):
        client.setex(redis_key, REDIS_TTL, value)

    return property(getter, setter)


@dataclass
class BadgeManager:
    user: User
    assignment: Assignment = None

    def __post_init__(self):
        self.user_profile = Profile.objects.get(user=self.user)

        self._user_storage = f"user:{self.user.id}"
        self._quests_key = self._user_storage + ":quests"
        self._badges_key = self._user_storage + ":badges"

        quest_config = [
            ("active_quests", "active", ":active"),
            ("success_quests", "success", ":success"),
            ("completed_quests", "completed", ":completed"),
            ("failed_quests", "failed", ":failed"),
        ]

        for prop_name, status, suffix in quest_config:
            key = self._quests_key + suffix
            setattr(self.__class__, prop_name, _make_quest_property(status, key))

    @property
    def all_quests(self) -> int:
        return self.active_quests + self.successful_quests + self.completed_quests + self.failed_quests

    def _has_badge(self, badge_slug: str) -> bool:
        badge_key = f"{self._badges_key}:{badge_slug}"

        if client.get(badge_key):
            print(f"Found {badge_slug} in cache")
            return True

        item = Badge.objects.filter(slug=badge_slug).first()
        exists = Profile.objects.filter(user=self.user, badges__in=[item]).exists()

        if exists:
            print(f"Doesn't found {badge_slug} in cache, but in db")
            client.setex(badge_key, REDIS_TTL, 1)
        return exists

    def _grant_badge(self, badge_slug: str) -> bool:
        if self._has_badge(badge_slug):
            return False

        try:
            key = f"{self._badges_key}:{badge_slug}"

            badge = Badge.objects.get(slug=badge_slug)

            self.user_profile.badges.add(badge)
            self.user_profile.save()

            # WARN: Delete at final ver.
            print(f"Granted badge: {badge_slug} for user: {self.user.username}")

            client.setex(key, REDIS_TTL, 1)
        except Exception:
            return False

    def badge_smartman(self):
        if self.success_quests >= 100:
            self._grant_badge("smartman")

    def badge_all_quests(self):
        if all(
            [self.active_quests > 0, self.success_quests > 0, self.completed_quests > 0, self.failed_quests > 0],
        ):
            self._grant_badge("jack_of_all_trades")

    def badge_pts(self):
        slug = checkers.check_pts(self.user_profile)
        self._grant_badge(slug)

    def check_all_badges(self):
        self.badge_smartman()
        self.badge_all_quests()
        self.badge_pts()

    def _flush(self):
        client.flushdb()
