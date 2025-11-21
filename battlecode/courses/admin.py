from django.contrib import admin
from .models import Course, CourseQuest

class CourseQuestInline(admin.TabularInline):
    model = CourseQuest
    extra = 0  # Убирает лишние пустые строки
    autocomplete_fields = ['quest']  # Удобно при большом количестве квестов

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [CourseQuestInline]
    list_display = ("title", "quest_count", "active", "updated_at", "created_at")
    list_filter = ("active", "updated_at", "created_at")
    search_fields = ("title", "description")
    readonly_fields = ("quest_count", "total_pts", "work_time", "updated_at", "created_at")
    prepopulated_fields = {"slug": ("title",)}  # Автозаполнение slug