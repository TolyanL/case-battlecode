from django.contrib import admin
from .models import Course, CourseQuest

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    search_fields = ['title']

class CourseQuestInline(admin.TabularInline):
    model = CourseQuest
    extra = 1

@admin.register(CourseQuest)
class CourseQuestAdmin(admin.ModelAdmin):
    list_display = ['course', 'quest', 'order']
    list_filter = ['course']