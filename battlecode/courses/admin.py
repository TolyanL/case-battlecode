from django.contrib import admin

from .models import Course, CourseQuest


class CourseQuestInline(admin.TabularInline):
    model = CourseQuest
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [CourseQuestInline]
