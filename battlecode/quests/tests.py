from hypothesis.extra import django

from django.contrib.auth.models import User
from django.shortcuts import reverse

from quests.models import Language, Quest, QuestReviewChecklist, Skill
from peer_review.models import Assignment


class TestQuestModel(django.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.language = Language.objects.create(name="Python", color="#3776ab")
        cls.checklist = QuestReviewChecklist.objects.create()
        cls.skill1 = Skill.objects.create(name="Skill 1", value=10)
        cls.skill2 = Skill.objects.create(name="Skil 2", value=5)

        cls.quest = Quest.objects.create(
            title="Title for Quest",
            description="Description",
            difficulty="medium",
            task="Solve it",
            base_pts=100,
            language=cls.language,
            checklist=cls.checklist,
        )
        cls.quest.skills.add(cls.skill1, cls.skill2)

    def test_pts(self):
        self.assertEqual(self.quest.pts, 140)


class SimpleQuestsViewTests(django.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="worker", password="pass123")

        language = Language.objects.create(name="Python", color="#000000")
        checklist = QuestReviewChecklist.objects.create()

        cls.quest = Quest.objects.create(
            title="Test Quest",
            description="Description",
            difficulty="easy",
            task="Solve it",
            language=language,
            checklist=checklist,
            active=True,
        )
        skill = Skill.objects.create(name="Skill", value=5)
        cls.quest.skills.add(skill)

    def test_quests_all_unauthenticated_see_quest(self):
        response = self.client.get(reverse("quests_all"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Quest")

    def test_quests_all_shows_quest_for_authenticated(self):
        self.client.login(username="worker", password="pass123")

        response = self.client.get(reverse("quests_all"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Quest")

    def test_quest_detail_redirects_unauthenticated(self):
        response = self.client.get(reverse("quest_detail", kwargs={"slug": self.quest.slug}))
        self.assertEqual(response.status_code, 302)

    def test_quest_detail_shows_for_authenticated(self):
        self.client.login(username="worker", password="pass123")

        response = self.client.get(reverse("quest_detail", kwargs={"slug": self.quest.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Quest")

    def test_quest_detail_has_start_button_by_default(self):
        self.client.login(username="worker", password="pass123")

        response = self.client.get(reverse("quest_detail", kwargs={"slug": self.quest.slug}))

        self.assertEqual(response.context["button_state"], "start")

    def test_quest_detail_has_continue_button_if_active_assignment(self):
        Assignment.objects.create(user=self.user, quest=self.quest, status="active")

        self.client.login(username="worker", password="pass123")

        response = self.client.get(reverse("quest_detail", kwargs={"slug": self.quest.slug}))
        self.assertEqual(response.context["button_state"], "continue_work")
