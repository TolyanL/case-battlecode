from hypothesis.extra import django

from courses.models import Course
from quests.models import Quest, Skill, Language, QuestReviewChecklist


class TestCourseModel(django.TestCase):
    @classmethod
    def setUpTestData(cls):
        language = Language.objects.create(name="Python", color="#000000")

        checklist1 = QuestReviewChecklist.objects.create()
        checklist2 = QuestReviewChecklist.objects.create()

        skill1 = Skill.objects.create(name="skill1", value=10)
        skill2 = Skill.objects.create(name="Skill2", value=5)
        skill3 = Skill.objects.create(name="Skill3", value=2)

        cls.quest1 = Quest.objects.create(
            title="Квест 1",
            description="Описание 1",
            difficulty="easy",
            task="Task",
            language=language,
            checklist=checklist1,
            work_time=2,
        )
        cls.quest1.skills.add(skill1)

        cls.quest2 = Quest.objects.create(
            title="Quest 2",
            description="Description",
            difficulty="medium",
            task="Task",
            language=language,
            checklist=checklist2,
            base_pts=200,
        )
        cls.quest2.skills.add(skill2, skill3)

        cls.course = Course.objects.create(
            title="Course Test",
            description="Description",
        )
        cls.course.quests.add(cls.quest1, cls.quest2)

    def test_course_quest_count(self):
        self.assertEqual(self.course.quest_count, 2)

    def test_course_skills(self):
        skills = list(self.course.skills)
        self.assertEqual(len(skills), 3)
        self.assertIn("Skill2", [s.name for s in skills])

    def test_course_total_pts(self):
        total = self.quest1.pts + self.quest2.pts
        self.assertEqual(self.course.total_pts, total)

    def test_course_work_time(self):
        self.assertEqual(self.course.work_time, 2 + 3)

    def test_course_active_default(self):
        self.assertTrue(self.course.active)

    def test_coursequest_order_default(self):
        course_quest1 = self.course.course_quests.get(quest=self.quest1)
        course_quest2 = self.course.course_quests.get(quest=self.quest2)

        self.assertEqual(course_quest1.order, 1)
        self.assertEqual(course_quest2.order, 1)
