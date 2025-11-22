from django.urls import path

from .views import dashboard, battle
from .requests import start_battle, ready


urlpatterns = [
    path("", dashboard, name="pvp_dashboard"),
    path("battle/<str:code>", battle, name="pvp_battle"),
    path("rest/start-battle", start_battle, name="pvp_battle_start"),
    path("rest/battle/change-state", ready, name="pvp_battle_ch_state"),
]
