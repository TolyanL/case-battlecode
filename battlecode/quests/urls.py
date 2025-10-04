from django.urls import path
from . import views

urlpatterns = [
    path("", views.quests_all, name="quests_all"),
    path("check", views.quests_check, name="quests_check"),
    path("<int:pk>/", views.quest_detail, name="quest_detail"),
]