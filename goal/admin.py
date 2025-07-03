from django.contrib import admin
from django.utils.html import format_html

from .models import Goal


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title', 
        'user',
        'deadline',
        'status',
        'completed_at',
        'verification_link'
    ]
    list_filter = ['status', 'deadline']
    search_fields = ['title', 'user__username', 'friendEmail']
    readonly_fields = ['verification_token', 'completed_at']
    
    fieldsets = (
        ('Goal Information', {
            'fields': ('title', 'description', 'deadline', 'friendEmail', 'user')
        }),
        ('Status', {
            'fields': ('status', 'completed_at')
        }),
        ('Verification', {
            'fields': ('verification_token',)
        }),
    )
    
    def verification_link(self, obj):
        if obj.verification_token:
            return format_html(
                '<a href="/api/goal/complete/{}" target="_blank">Verify Goal</a>',
                obj.verification_token
            )
        return "No token"
    verification_link.short_description = "Verification Link"
