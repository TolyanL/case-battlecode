from django.contrib import admin

from .models import Assignment, CourseProgress, Review, ReviewChecklistAnswer


@admin.register(CourseProgress)
class CourseProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "status", "completed_at", "updated_at", "created_at")
    list_filter = ("user", "status", "course", "completed_at", "updated_at", "created_at")

    ordering = ["-updated_at"]
    date_hierarchy = "updated_at"


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("user", "quest", "status", "completed_at", "updated_at", "assigned_at")
    list_filter = ("user", "status", "quest", "completed_at", "updated_at", "assigned_at")

    ordering = ["-assigned_at"]
    date_hierarchy = "assigned_at"


class ReviewChecklistAnswerInline(admin.TabularInline):
    model = ReviewChecklistAnswer
    extra = 1


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    inlines = [ReviewChecklistAnswerInline]

    list_display = ("user", "assignment", "completed_tasks", "grade", "comment", "give_pts", "updated_at", "created_at")
    list_filter = ("user", "assignment", "grade", "give_pts", "updated_at", "created_at")

    ordering = ["-updated_at"]
    date_hierarchy = "updated_at"
