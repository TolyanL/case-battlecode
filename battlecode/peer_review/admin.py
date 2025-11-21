from django.contrib import admin
from .models import Assignment, CourseProgress, Review, ReviewChecklistAnswer

@admin.register(CourseProgress)
class CourseProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "status", "progress_percent", "completed_at", "updated_at", "created_at")
    list_filter = ("status", "course", "completed_at", "updated_at", "created_at")
    search_fields = ("user__username", "course__title")
    ordering = ["-updated_at"]
    date_hierarchy = "updated_at"
    autocomplete_fields = ['user', 'course'] # Удобно при большом количестве

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("user", "quest", "status", "given_pts", "reviews", "reviews_avg_pts", "completed_at", "updated_at", "assigned_at")
    list_filter = ("status", "quest", "completed_at", "updated_at", "assigned_at")
    search_fields = ("user__username", "quest__title")
    ordering = ["-assigned_at"]
    date_hierarchy = "assigned_at"
    autocomplete_fields = ['user', 'quest'] # Удобно при большом количестве
    readonly_fields = ("given_pts", "completed_at", "updated_at", "assigned_at", "reviews", "reviews_avg_pts")

class ReviewChecklistAnswerInline(admin.TabularInline):
    model = ReviewChecklistAnswer
    extra = 0

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    inlines = [ReviewChecklistAnswerInline]
    list_display = ("user", "assignment", "grade", "give_pts", "updated_at", "created_at")
    list_filter = ("grade", "give_pts", "updated_at", "created_at")
    search_fields = ("user__username", "assignment__quest__title")
    ordering = ["-updated_at"]
    date_hierarchy = "updated_at"
    autocomplete_fields = ['user', 'assignment'] # Удобно при большом количестве
    readonly_fields = ("updated_at", "created_at")