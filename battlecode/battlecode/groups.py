from dataclasses import dataclass

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


# Uncomment next lines and add to the group.perms_model if nessesary
# from user.models import Profile
# from peer_review.models import Assignment, Review, ReviewChecklistAnswer

from badges.models import Badge
from courses.models import Course, CourseQuest
from quests.models import Quest, Skill, Language, ChecklistItem, QuestReviewChecklist


@dataclass
class BCGroup:
    name: str
    verbose_name: str
    verbose_name_plural: str
    perms_models: list[object]
    exlude_perms: list[str] | None = None

    def get_content_types(self) -> list[ContentType]:
        if not len(self.perms_models):
            return []
        if self.perms_models[0] == "all":
            return list(Permission.objects.all().values_list("content_type", flat=True))

        cts = []
        for m in self.perms_models:
            cts.append(ContentType.objects.get_for_model(m))

        return cts

    def get_permissions(self) -> list[Permission]:
        if not len(self.perms_models):
            return []
        if self.perms_models[0] == "all":
            return list(Permission.objects.all())

        group_perms = []
        for m in self.perms_models:
            ct = ContentType.objects.get_for_model(m)
            perms = Permission.objects.filter(content_type=ct).all()

            if self.exlude_perms:
                perms = perms.exclude(codename__in=self.exlude_perms)

            group_perms.extend(perms)

        return group_perms


STUDENT_GROUP = "students"
TEACHER_GROUP = "teachers"
ADMIN_GROUP = "admins"

GROUPS: list[BCGroup] = [
    BCGroup(
        name=ADMIN_GROUP,
        verbose_name="Администраторы",
        verbose_name_plural="Администратор",
        perms_models=["all"],
    ),
    BCGroup(
        name=TEACHER_GROUP,
        verbose_name="Преподаватели",
        verbose_name_plural="Преподаватель",
        perms_models=[
            Badge,
            Course,
            CourseQuest,
            Quest,
            Skill,
            Language,
            ChecklistItem,
            QuestReviewChecklist,
        ],
    ),
    BCGroup(
        name=STUDENT_GROUP,
        verbose_name="Студенты",
        verbose_name_plural="Студент",
        perms_models=[],
    ),
]

DEFAULT_USER_GROUP = STUDENT_GROUP
