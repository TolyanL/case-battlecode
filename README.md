# Overview

BattleCode is a gamified coding education platform that combines structured learning paths with peer review evaluation. Users complete coding quests, participate in courses, earn badges, and compete on leaderboards. The platform enforces quality through a mandatory peer review system where submissions are evaluated by other participants using structured checklists.


## System Purpose

The platform provides:

*   **Quest Management**: Individual coding challenges with difficulty levels, time limits, and point rewards.
*   **Course Organization**: Structured learning paths grouping quests in a specific order.
*   **Peer Review Workflow**: Community-driven quality assurance through structured evaluations.
*   **Progression System**: Points, ranks, and badges that track user advancement.
*   **Competitive Features**: Public leaderboards displaying user rankings and statistics.


## High-Level Architecture

![alt text](/docs/img/high-level-architecture.png)

**Container Architecture**: The system runs as five Docker containers defined in `docker-compose.dev.yaml`:

*   `case_db`: PostgreSQL database with persistent volume `postgres_data`.
*   `case_redis`: Redis server for caching and Celery message brokering.
*   `case_web`: Django application served via Gunicorn.
*   `case_celery_worker`: Asynchronous task processor.
*   `case_celery_beat`: Periodic task scheduler.


## Core Data Model

![alt text](/docs/img/core-data-model.png)

**Key Models**:

*   **Quest**: Atomic coding challenge with `slug`, `difficulty`, `base_pts`, `penalty`, and `work_time` attributes.
*   **Assignment**: User's attempt at a quest with `status` field tracking lifecycle: `active` → `completed` → `success`/`failed`.
*   **Review**: Peer evaluation containing `grade`, `give_pts`, and structured `ReviewChecklistAnswer` items.
*   **Course**: Learning path with ordered quest sequence.
*   **CourseProgress**: Per-user tracking of course completion with `status` field.
*   **Profile**: User statistics including `pts` (points), `rank_as_str`, and `placement`.
*   **Badge**: Achievement awards linked to quests and courses.


## Application Flow

![alt text](/docs/img/application-flow.png)

**View Controllers**:

*   **QuestsAllView**: Lists available quests filtered by user's course enrollments and assignment status (`active`, `completed`, `on_cooldown`, `available`).
*   **QuestDetailView**: Displays quest details with dynamic button states based on current `Assignment` status.
*   **QuestWorkView**: Provides CodeMirror editor for code submission with timer display.

**Action Endpoints** (called via AJAX from `buttons.js`):

*   `accept_quest(slug)`: Creates new `Assignment` with `status='active'`.
*   `complete_quest(slug)`: Updates `Assignment` to `status='completed'`, queues for review.
*   `give_up_quest(slug)`: Sets `Assignment` to `status='failed'`, applies `quest.penalty` to user points.


## Technology Stack

| Component | Technology | Purpose | Configuration |
| :--- | :--- | :--- | :--- |
| **Web Framework** | Django 5.2.7 | Application logic, ORM, templates | [settings.py](https://github.com/TolyanL/case-battlecode/blob/bcde6f35/settings.py#L1-L252) |
| **Web Server** | Gunicorn 23.0.0 | WSGI server | [pyproject.toml](https://github.com/TolyanL/case-battlecode/blob/bcde6f35/pyproject.toml#L18-L18) |
| **Database** | PostgreSQL 17 | Primary data store | [settings.py](https://github.com/TolyanL/case-battlecode/blob/bcde6f35/settings.py#L102-L111) |
| **Cache/Queue** | Redis Alpine | Session storage, Celery broker | [settings.py](https://github.com/TolyanL/case-battlecode/blob/bcde6f35/settings.py#L116-L127) |
| **Task Queue** | Celery 5.5.3 | Background job processing | [settings.py](https://github.com/TolyanL/case-battlecode/blob/bcde6f35/settings.py#L130-L150) |
| **Frontend CSS** | Tailwind CSS | Utility-first styling | [templates/base.html](https://github.com/TolyanL/case-battlecode/blob/bcde6f35/templates/base.html#L19-L19) |
| **Code Editor** | CodeMirror 5.65.2 | In-browser code editing | [templates/base.html](https://github.com/TolyanL/case-battlecode/blob/bcde6f35/templates/base.html#L21-L21) |
| **2FA** | django-otp + django-two-factor-auth | Two-factor authentication | [settings.py](https://github.com/TolyanL/case-battlecode/blob/bcde6f35/settings.py#L41-L44) |
| **Admin UI** | django-simpleui | Enhanced admin interface | [settings.py](https://github.com/TolyanL/case-battlecode/blob/bcde6f35/settings.py#L33-L33) |

**Celery Configuration**:

```python
CELERY_BROKER_URL = "redis://case_redis:6379/0"
CELERY_BEAT_SCHEDULE = {
    "check-expired-assigments": {
        "task": "peer_review.tasks.check_assignments",
        "schedule": timedelta(minutes=1)
    },
    "check-finished-courses": {
        "task": "courses.tasks.check_finished_courses", 
        "schedule": timedelta(minutes=5)
    }
}
```

**Periodic Tasks**:

*   `check_assignments`: Scans active assignments for deadline violations, automatically fails overdue submissions.
*   `check_finished_courses`: Detects course completions, awards course badges via `BadgeManager`.


## Key Features

### Quest System

Coding challenges with configurable parameters:

*   **Difficulty Levels**: `easy`, `medium`, `hard` (displayed with color-coded badges).
*   **Point Rewards**: `base_pts` awarded on success.
*   **Penalties**: Optional `penalty` points deducted on failure or timeout.
*   **Time Limits**: `work_time` (in hours) enforced by background task.
*   **Skills**: Many-to-many relationship with `Skill` model.
*   **Language**: Foreign key to `Language` model with `bg_color` and `color` fields.

### Peer Review System

Community-driven evaluation process:

*   Each completed assignment enters review queue.
*   Multiple users evaluate using structured `QuestReviewChecklist`.
*   Reviews include numeric `grade` and text `comment`.
*   Points calculated via `give_pts` field based on checklist answers.
*   Average review score determines success/failure threshold.

### Course System

Structured learning paths:

*   Ordered sequence of quests (`CourseQuest` join table).
*   Per-user `CourseProgress` tracking with `completed_quests_count`.
*   Automatic completion detection when all quests finished.
*   Course-specific badges awarded upon completion.
*   Enrollment controls quest visibility in `QuestsAllView`.

### Progression System

User advancement mechanics:

*   **Points**: Accumulated via successful quest completion, stored in `Profile.pts`.
*   **Ranks**: Defined in `stats_settings.py`, calculated from point thresholds.
*   **Badges**: Awarded for quest completion and course milestones.
*   **Placement**: Leaderboard position stored in `Profile.placement`.
*   **Statistics**: Total work time, preferred languages, recent activity.


## Navigation Structure

![alt text](/docs/img/navigation-structure-diagram.png)

**Menu Implementation**: The navigation menu in `templates/include/menu.html` displays current page highlighting using `pd.curr_page` context variable. User information shows username, rank (`user.profile.rank_as_str`), and points (`user.profile.pts`).

**Authentication**: All views except landing page require `LoginRequiredMixin` or `@login_required` decorator. Two-factor authentication enforced via `django_otp.middleware.OTPMiddleware`.


## Template Inheritance

![alt text](/docs/img/template-inheritance.png)

**Base Template**: `templates/base.html` provides:

*   Header with navigation menu.
*   Tailwind CSS configuration.
*   Feather icons library.
*   CodeMirror script inclusion.
*   Mobile-responsive layout.
*   Common JavaScript utilities.

**Static Assets**: Loaded from `static/` directory including:

*   `css/styles.css`: Custom styles.
*   `js/tailwind.js`: Tailwind configuration.
*   `js/buttons.js`: Quest action handlers.
*   `js/mobile-menu.js`: Responsive menu toggle.