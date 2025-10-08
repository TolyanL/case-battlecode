# battlecode/user/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from battlecode.pagedata import PageData
from quests.models import Assignment # Импортируем Assignment

@login_required  # только для авторизованных — иначе "me" не имеет смысла
def user_profile(request, username: str):
    if username == "me":
        # Если запрашивается /profile/me/ — показываем профиль текущего пользователя
        profile_user = request.user
    else:
        # Иначе ищем пользователя по реальному username
        profile_user = get_object_or_404(User, username=username)

    # Убедимся, что у пользователя есть профиль (обычно создаётся сигналом, но на всякий случай)
    profile = getattr(profile_user, 'profile', None)
    if profile is None:
        # Можно создать профиль автоматически или выдать ошибку
        from user.models import Profile
        profile = Profile.objects.create(user=profile_user)

    # --- НОВАЯ ЛОГИКА: Цвета для сложности ---
    # Словарь, связывающий difficulty с CSS-классами
    DIFFICULTY_COLORS = {
        'easy': {'bg': 'bg-green-500/20', 'text': 'text-green-500'},
        'medium': {'bg': 'bg-orange-500/20', 'text': 'text-orange-500'},
        'hard': {'bg': 'bg-red-500/20', 'text': 'text-red-500'},
        # По умолчанию
        'default': {'bg': 'bg-gray-500', 'text': 'text-white'}
    }

    # Получаем последние Assignment для этого User
    assignments = Assignment.objects.filter(user=profile_user).order_by('-assigned_at')[:5]
    # Добавляем цвет сложности к каждому assignment
    for assignment in assignments:
        difficulty = assignment.quest.difficulty
        assignment.difficulty_color = DIFFICULTY_COLORS.get(difficulty, DIFFICULTY_COLORS['default'])

    # Для "Недавней активности"
    recent_activities = Assignment.objects.filter(
        user=profile_user
    ).exclude( # Исключаем не начатые
        status='not_started'
    ).order_by('-assigned_at')[:3]
    # Добавляем цвет сложности к каждому recent_activity
    for activity in recent_activities:
        difficulty = activity.quest.difficulty
        activity.difficulty_color = DIFFICULTY_COLORS.get(difficulty, DIFFICULTY_COLORS['default'])

    # --- НОВАЯ ЛОГИКА: Подсчёт предпочтительных языков ---
    # Группируем Assignments по языку и считаем количество
    language_counts = {}
    for assignment in assignments: # Или можно использовать all() для всех квестов
        lang_name = assignment.quest.language.name
        if lang_name in language_counts:
            language_counts[lang_name] += 1
        else:
            language_counts[lang_name] = 1

    # Рассчитываем проценты и углы для диаграммы
    total_assignments = sum(language_counts.values())
    preferred_languages = []
    if total_assignments > 0:
        cumulative_percentage = 0 # Для отслеживания накопленного процента
        for lang_name, count in language_counts.items():
            percentage = int((count / total_assignments) * 100)
            # Рассчитываем углы в градусах (360 градусов * процент / 100)
            start_angle = cumulative_percentage * 360 / 100
            cumulative_percentage += percentage
            end_angle = cumulative_percentage * 360 / 100
            # Длина дуги в "условных единицах" (где полная окружность = 100)
            dash_array_length = percentage
            # Остаток до 100
            dash_array_gap = 100 - percentage
            # Сдвиг начала штриха (в "условных единицах")
            # Для круговой диаграммы: stroke-dashoffset = - (start_angle_deg / 360) * 100
            dash_offset = - (start_angle / 360) * 100
            preferred_languages.append({
                'name': lang_name,
                'percentage': percentage,
                'count': count,
                'start_angle': start_angle,
                'end_angle': end_angle,
                'dash_array_length': dash_array_length,
                'dash_array_gap': dash_array_gap,
                'dash_offset': dash_offset,
            })

    # Сортируем по проценту (убывание)
    preferred_languages.sort(key=lambda x: x['percentage'], reverse=True)

    # Заглушка для очков за квесты
    quest_points_info = "Здесь будут отображаться очки за квесты (заглушка)."

    pd = PageData(
        title=f"Профиль — {profile_user.username}",
        description=f"Страница профиля пользователя {profile_user.username}.",
        curr_page="user",
    )

    return render(request, "user_profile.html", context={
        "pd": pd,
        "profile_user": profile_user,
        "profile": profile,
        "assignments": assignments,
        "recent_activities": recent_activities,
        "preferred_languages": preferred_languages,
        "quest_points_info": quest_points_info,
        # Не нужно передавать DIFFICULTY_COLORS, так как цвета уже в assignment и recent_activity
    })
