from django.utils import timezone
from hypothesis.extra import django

from django.contrib.auth.models import User

from user.models import Profile
from courses.models import Course
from quests.models import Quest, Language, QuestReviewChecklist, Skill
from peer_review.models import Assignment, CourseProgress, Review


class TestAssignmentModel(django.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser")

        cls.rev_user1 = User.objects.create_user(username="review user 1")
        cls.rev_user2 = User.objects.create_user(username="review user 2")
        cls.rev_user3 = User.objects.create_user(username="review user 3")

        cls.profile = Profile.objects.create(user=cls.user, pts=0)

        language = Language.objects.create(name="Test Lang", color="#fff")
        checklist = QuestReviewChecklist.objects.create()
        skill = Skill.objects.create(name="Test", value=5)

        cls.quest = Quest.objects.create(
            title="Test Quest",
            description="Description",
            difficulty="easy",
            task="Task",
            language=language,
            checklist=checklist,
            base_pts=100,
            penalty=10,
            work_time=1,
        )
        cls.quest.skills.add(skill)

        cls.assignment = Assignment.objects.create(
            user=cls.user,
            quest=cls.quest,
            code="test code",
            status="active",
        )

    def test_reviews_count(self):
        self.assertEqual(self.assignment.reviews, 0)

        Review.objects.create(
            user=self.rev_user1,
            assignment=self.assignment,
            give_pts=80,
        )
        Review.objects.create(
            user=self.rev_user2,
            assignment=self.assignment,
            give_pts=90,
        )

        self.assertEqual(self.assignment.reviews, 2)

    def test_reviews_avg_pts(self):
        Review.objects.create(
            user=self.rev_user1,
            assignment=self.assignment,
            give_pts=80,
        )
        Review.objects.create(
            user=self.rev_user2,
            assignment=self.assignment,
            give_pts=90,
        )

        self.assertEqual(self.assignment.reviews_avg_pts, 85)

        Review.objects.create(
            user=self.rev_user3,
            assignment=self.assignment,
            give_pts=90,
        )
        self.assertEqual(self.assignment.reviews_avg_pts, 86)

    def test_finish_success(self):
        Review.objects.create(
            user=self.rev_user1,
            assignment=self.assignment,
            give_pts=70,
        )
        self.assignment.finish()

        self.assertEqual(self.assignment.status, "success")
        self.assertEqual(self.assignment.given_pts, 70)

        self.profile.refresh_from_db()

        self.assertEqual(self.profile.pts, 70)
        self.assertIsNotNone(self.assignment.completed_at)

    def test_finish_failed_due_to_low_reviews(self):
        Review.objects.create(
            user=self.rev_user1,
            assignment=self.assignment,
            give_pts=0,
        )
        self.assignment.finish()

        self.assertEqual(self.assignment.status, "failed")
        self.assertEqual(self.assignment.given_pts, -10)

        self.profile.refresh_from_db()

        self.assertEqual(self.profile.pts, 0)

    def test_fail_method(self):
        self.assignment.fail()

        self.assertEqual(self.assignment.status, "failed")
        self.assertEqual(self.assignment.given_pts, 0)

        self.profile.refresh_from_db()

        self.assertEqual(self.profile.pts, 0)
        self.assertIsNotNone(self.assignment.completed_at)


class TestCourseProgressModel(django.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="student")
        cls.profile = Profile.objects.create(user=cls.user)

        language = Language.objects.create(name="Test Lang", color="#fff")

        checklist1 = QuestReviewChecklist.objects.create()
        checklist2 = QuestReviewChecklist.objects.create()

        cls.course = Course.objects.create(title="Test Course")
        cls.quest1 = Quest.objects.create(
            title="Quest 1",
            description="Description",
            difficulty="easy",
            task="Task",
            language=language,
            checklist=checklist1,
            base_pts=50,
            work_time=1,
        )
        cls.quest2 = Quest.objects.create(
            title="Quest 2",
            description="Description",
            difficulty="medium",
            task="Task",
            language=language,
            checklist=checklist2,
            base_pts=100,
            work_time=2,
        )
        cls.course.quests.add(cls.quest1, cls.quest2)

        cls.progress = CourseProgress.objects.create(user=cls.user, course=cls.course)

        Assignment.objects.create(
            user=cls.user,
            quest=cls.quest1,
            code="test",
            status="success",
            completed_at=timezone.now(),
        )

    def test_completed_quests_count(self):
        self.assertEqual(self.progress.completed_quests_count, 1)

    def test_progress_percent(self):
        self.assertEqual(self.progress.progress_percent, 50)

    def test_progress_percent_empty_course(self):
        empty_course = Course.objects.create(title="Empty Course")
        progress = CourseProgress.objects.create(user=self.user, course=empty_course)
        self.assertEqual(progress.progress_percent, 0)

    def test_complete_course(self):
        self.progress.complete()
        self.assertEqual(self.progress.status, "success")
        self.assertIsNotNone(self.progress.completed_at)
