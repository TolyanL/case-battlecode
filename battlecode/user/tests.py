from datetime import timedelta
from django.utils import timezone
from hypothesis import given
from hypothesis.extra import django

from django.contrib.auth.models import Group, User

from battlecode.stats_settings import RANKS
from battlecode.groups import STUDENT_GROUP

from peer_review.models import Assignment
from quests.models import Quest, Language, QuestReviewChecklist
from badges.models import Badge
from user.models import Profile


class TestProfileModel(django.TestCase):
    @given(django.from_model(User))
    def test_rank(self, instance: User):
        profile = Profile.objects.create(user=instance)

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

    @given(django.from_model(User))
    def test_rank_neg(self, instance: User):
        profile = Profile.objects.create(user=instance)

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
