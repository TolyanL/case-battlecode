from datetime import timedelta

from hypothesis import given, settings
from hypothesis.extra import django

from django.test import Client
from django.utils import timezone
from django.shortcuts import reverse
from django.contrib.auth.models import Group, User

from battlecode.stats_settings import RANKS
from battlecode.groups import STUDENT_GROUP

from peer_review.models import Assignment
from quests.models import Quest, Language, QuestReviewChecklist
from badges.models import Badge
from user.models import Profile


class TestProfileModel(django.TestCase):
    def test_rank(self):
        user = User.objects.create(username="worker")
        profile = Profile.objects.create(user=user)

        rank_1 = RANKS[0][1][7:].lower().strip()
        rank_2 = RANKS[9][1][7:].lower().strip()

        Badge.objects.create(name=rank_1, slug=rank_1)
        Badge.objects.create(name=rank_2, slug=rank_2)

        profile.pts = 100

        self.assertEqual(profile.rank, 1)
        self.assertEqual(profile.rank_as_str, rank_1)

        profile.pts = 5000
        self.assertEqual(profile.rank, 10)
        self.assertEqual(profile.rank_as_str, rank_2)

    def test_rank_neg(self):
        user = User.objects.create(username="worker")
        profile = Profile.objects.create(user=user)

        profile.pts = -100
        profile.save()

        self.assertEqual(profile.pts, 0)
        self.assertEqual(profile.rank, 1)
        self.assertEqual(profile.rank_as_str, "Unknown")

    def test_placement(self):
        def test_placement(self):
            student_group, _ = Group.objects.get_or_create(name=STUDENT_GROUP)

            u1 = User.objects.create(username="u1")
            u1.groups.add(student_group)
            p1 = Profile.objects.create(user=u1, pts=100)

            u2 = User.objects.create(username="u2")
            u2.groups.add(student_group)
            p2 = Profile.objects.create(user=u2, pts=200)

            self.assertEqual(p2.placement, 1)
            self.assertEqual(p1.placement, 2)

    def test_total_worktime(self):
        user = User.objects.create(username="worker")
        lang = Language.objects.create(name="Python", color="#3776ab")
        checklist = QuestReviewChecklist.objects.create()
        quest = Quest.objects.create(
            title="Test Quest",
            description="Desc",
            difficulty="medium",
            task="Solve it",
            language=lang,
            checklist=checklist,
        )

        now = timezone.now()

        a1 = Assignment(user=user, quest=quest, status="success")
        a1.save()
        Assignment.objects.filter(pk=a1.pk).update(
            assigned_at=now - timedelta(hours=2),
            completed_at=now,
        )

        a2 = Assignment(user=user, quest=quest, status="failed")
        a2.save()
        Assignment.objects.filter(pk=a2.pk).update(
            assigned_at=now - timedelta(hours=1, minutes=30),
            completed_at=now,
        )

        profile = Profile.objects.create(user=user)
        work_time = profile.total_worktime

        self.assertAlmostEqual(work_time, 3.5, places=2)


class TestUserProfileView(django.TestCase):
    def test_user_profile_me(self):
        user = User.objects.create_user(username="testuser", password="secret")
        lang = Language.objects.create(name="Python", color="#3776ab")
        checklist = QuestReviewChecklist.objects.create()
        quest = Quest.objects.create(
            title="Test Quest",
            description="Desc",
            difficulty="easy",
            task="Code it",
            language=lang,
            checklist=checklist,
        )

        now = timezone.now()
        assignment = Assignment(user=user, quest=quest, status="success")
        assignment.save()
        Assignment.objects.filter(pk=assignment.pk).update(assigned_at=now - timedelta(hours=1), completed_at=now)

        client = Client()
        client.login(username="testuser", password="secret")

        response = client.get(reverse("user_profile", kwargs={"username": "me"}))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["user"].username, "testuser")
        self.assertIsInstance(response.context["profile"], Profile)
        self.assertEqual(response.context["total_assignments"], 1)
        self.assertEqual(len(response.context["recent_activities"]), 1)
        self.assertEqual(len(response.context["preferred_languages_text"]), 1)

    def test_user_profile_other_user(self):
        User.objects.create_user(username="viewer", password="secret")
        target = User.objects.create_user(username="target", password="secret2")

        client = Client()
        client.login(username="viewer", password="secret")

        response = client.get(reverse("user_profile", kwargs={"username": "target"}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user"].username, "target")
        self.assertTrue(hasattr(target, "profile"))

    @given(django.from_model(User))
    @settings(deadline=None)
    def test_user_profile_exists_for_any_user(self, user: User):
        Profile.objects.get_or_create(user=user)

        group, _ = Group.objects.get_or_create(name=STUDENT_GROUP)
        user.groups.add(group)

        lang = Language.objects.create(name="JS", color="#f1e05a")
        checklist = QuestReviewChecklist.objects.create()
        quest = Quest.objects.create(
            title=f"Quest for {user.username}",
            description="Auto",
            difficulty="medium",
            task="Return 42",
            language=lang,
            checklist=checklist,
        )

        now = timezone.now()
        ass = Assignment(user=user, quest=quest, status="success")
        ass.save()
        Assignment.objects.filter(pk=ass.pk).update(assigned_at=now - timedelta(minutes=30), completed_at=now)

        user.set_password("pass")
        user.save()
        client = Client()
        client.login(username=user.username, password="pass")

        response = client.get(reverse("user_profile", kwargs={"username": "me"}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user"].id, user.id)
        self.assertGreaterEqual(response.context["profile"].total_worktime, 0)
