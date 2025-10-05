from django.contrib import admin
from .models import Quest

@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at',)
    fieldsets = (
        (None, {
            'fields': ('title', 'description')
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    ordering = ['-created_at']
    date_hierarchy = 'created_at'