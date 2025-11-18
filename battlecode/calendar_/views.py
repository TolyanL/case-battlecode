from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.db.models import Q

from peer_review.models import Assignment


@login_required
def calendar(request):
    now = timezone.now()
    today = now.date()

    start_date = today - timedelta(days=2)
    end_date = today + timedelta(days=4)

    fetch_start_date = start_date - timedelta(days=10)

    major_hours = [0, 6, 9, 12, 15, 18, 21]

    week_days = []
    days_map = {}

    current_date = start_date
    while current_date <= end_date:
        day_data = {
            "date": current_date.strftime("%d.%m"),
            "name": current_date.strftime("%A"),
            "is_current": current_date == today,
            "is_past": current_date < today,
            "time_blocks": {hour: [] for hour in major_hours},
        }
        week_days.append(day_data)
        days_map[current_date] = day_data
        current_date += timedelta(days=1)

    assignments = (
        Assignment.objects.filter(
            Q(user=request.user),
            (
                Q(status__in=["active", "in_progress", "on_review"])
                & Q(assigned_at__date__gte=fetch_start_date)
                & Q(assigned_at__date__lte=end_date)
            )
            | (
                Q(status__in=["success", "failed"])
                & Q(completed_at__date__gte=start_date)
                & Q(completed_at__date__lte=end_date)
            ),
        )
        .select_related("quest", "quest__language")
        .prefetch_related("quest__skills")
        .distinct()
    )

    for assignment in assignments:
        utc_timestamp = None
        if assignment.status in ["success", "failed"] and assignment.completed_at:
            utc_timestamp = assignment.completed_at
        elif assignment.quest.work_time:
            utc_timestamp = assignment.assigned_at + timedelta(hours=assignment.quest.work_time)
        else:
            continue

        local_timestamp = timezone.localtime(utc_timestamp)
        timestamp_date = local_timestamp.date()
        timestamp_hour = local_timestamp.hour

        if timestamp_date in days_map:
            block_start_hour = 0
            for hour in major_hours:
                if timestamp_hour >= hour:
                    block_start_hour = hour
                else:
                    break

            day_data = days_map[timestamp_date]

            event_info = {"quest": assignment.quest, "assignment": assignment, "deadline": local_timestamp}
            day_data["time_blocks"][block_start_hour].append(event_info)

    context = {
        "week_days": week_days,
        "hours_range": major_hours,
    }

    return render(request, "calendar.html", context)

