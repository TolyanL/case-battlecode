from django.contrib import admin

from .models import Assignment, Review, ReviewChecklistAnswer


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("user", "quest", "status", "assigned_at")
    list_filter = ("status", "assigned_at")

    ordering = ["-assigned_at"]
    date_hierarchy = "assigned_at"


class ReviewChecklistAnswerInline(admin.TabularInline):
    model = ReviewChecklistAnswer
    extra = 1


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    inlines = [ReviewChecklistAnswerInline]

    list_display = ("user", "assignment", "completed_tasks", "grade", "comment", "give_pts", "updated_at", "created_at")
    list_filter = ("assignment", "grade", "updated_at")

    ordering = ["-updated_at"]
    date_hierarchy = "updated_at"
