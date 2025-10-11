from django.urls import path
from .views import (
    quests_all,
    QuestDetailView,
    QuestWorkView,
    quest_reviews,
    # courses_all,
    # CourseDetailView,
    # enroll_course,
    # unenroll_course,
)
from .requests import accept_quest, give_up_quest, complete_quest

urlpatterns = [
    path("", quests_all, name="quests_all"),
    path("details/<str:slug>", QuestDetailView.as_view(), name="quest_detail"),
    path("work/<str:slug>", QuestWorkView.as_view(), name="quest_work"),
    path("reviews/<str:slug>", quest_reviews, name="quest_reviews"),
    path("accept", accept_quest, name="req_accept_quest"),
    path("give-up", give_up_quest, name="req_give_up"),
    path("complete", complete_quest, name="req_complete_quest"),
    # path("courses/", courses_all, name="courses_all"),
    # path("courses/details/<str:slug>", CourseDetailView.as_view(), name="course_detail"),
    # path("courses/enroll", enroll_course, name="req_enroll_course"),
    # path("courses/unenroll", unenroll_course, name="req_unenroll_course"),
]
