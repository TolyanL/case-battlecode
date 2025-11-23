from django.urls import path

from .views import dashboard, battle, do_task, results
from .requests import start_battle, change_state, skip, fail, complete


urlpatterns = [
    path("", dashboard, name="pvp_dashboard"),
    path("battle/<str:code>", battle, name="pvp_battle"),
    path("battle/<str:code>/do", do_task, name="pvp_battle_do"),
    path("battle/<str:code>/results", results, name="pvp_battle_results"),
    # rest
    path("rest/start-battle", start_battle, name="pvp_battle_start"),
    path("rest/battle/change-state", change_state, name="pvp_battle_ch_state"),
    path("rest/battle/skip", skip, name="pvp_battle_skip"),
    path("rest/battle/complete", complete, name="pvp_battle_complete"),
    path("rest/battle/fail", fail, name="pvp_battle_fail"),
]
