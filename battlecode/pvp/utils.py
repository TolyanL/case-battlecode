from random import choice

from django.utils import timezone
from django.contrib.auth.models import User

from user.models import Profile

from battlecode.redis_settings import client
from battlecode.pvp_settings import REDIS_TTL, LEVEL_DELTA

from ai.client import AIClient


def last_users() -> list[User]:
    last_users = []
    now = timezone.now() - timezone.timedelta(minutes=REDIS_TTL / 60)

    for u in User.objects.filter().all():
        val = client.get(f"user-last-active-{u.id}")
        if not val:
            continue

        last_login = float(val)
        if last_login > now.timestamp():
            last_users.append(u)

    return last_users


def get_opponent(curr_user: User, users: list[User]) -> User | None:
    fits = []

    for u in users:
        # WARN: uncomment this line in final version
        # if u.id == curr_user.id:
        #     continue

        curr_p = Profile.objects.get(user=curr_user)
        p = Profile.objects.get(user=u)

        if curr_p.pts - LEVEL_DELTA <= p.pts <= curr_p.pts + LEVEL_DELTA:
            fits.append(u)

    if not fits:
        return None

    return choice(fits)


def evaluate_solution(user_code: str, opponent_code: str, max_pts: int) -> str:
    prompt = """Ты — эксперт по оценке кода в соревновательном программировании.
        Твоя задача — объективно сравнить два решения одной и той же задачи.
        Оцени каждое решение по совокупности: правильность, красота, лаконичность, размер.
        Вычисли, насколько каждое решение близко к 'идеальному' эталону:
        идеальный код — это максимально лаконичный, читаемый, корректный и эффективный код.
        Используй максимальный балл: {max_pts}. СТРОГО без своих комментариев.
        Выведи ТОЛЬКО финальные баллы за задания в формате: <USER 1 PTS>|<USER 2 PTS>

        Заданиие 1 пользователя:
        ```
        {task_1}
        ```

        Заданиие 2 пользователя:
        ```
        {task_2}
        ```
        """

    print(
        prompt.format(
            max_pts=max_pts,
            task_1=user_code,
            task_2=opponent_code,
        )
    )
    return

    response = AIClient.chat_response(
        prompt.format(
            max_pts=max_pts,
            task_1=user_code,
            task_2=opponent_code,
        )
    )

    import json

    result = json.loads(response)
    return result["final_score_a"]["absolute"]
