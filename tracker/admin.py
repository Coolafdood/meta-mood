from django.contrib import admin
from .models import Reason, Action, MoodEntry


@admin.register(Reason)
class ReasonAdmin(admin.ModelAdmin):
    list_display = ["text", "mood_type", "category", "is_generic", "created_at"]
    list_filter = ["mood_type", "category", "is_generic"]
    search_fields = ["text"]
    list_editable = ["mood_type", "category", "is_generic"]

    fieldsets = (
        ("Reason Details", {"fields": ("text", "mood_type", "category", "is_generic")}),
    )


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ["text", "category", "is_generic", "created_at"]
    list_filter = ["category", "is_generic", "reasons__mood_type"]
    search_fields = ["text"]
    filter_horizontal = ["reasons"]

    fieldsets = (
        ("Action Details", {"fields": ("text", "category", "is_generic")}),
        (
            "Related Reasons",
            {
                "fields": ("reasons",),
                "description": "Select which reasons this action applies to",
            },
        ),
    )


@admin.register(MoodEntry)
class MoodEntryAdmin(admin.ModelAdmin):
    list_display = ["user", "mood", "reason", "action", "action_worked", "created_at"]
    list_filter = ["mood", "action_worked", "created_at"]
    search_fields = ["user__username", "notes"]
    date_hierarchy = "created_at"

    fieldsets = (
        ("User Info", {"fields": ("user",)}),
        ("Mood Data", {"fields": ("mood", "reason", "action", "notes")}),
        (
            "Effectiveness",
            {
                "fields": ("action_worked", "action_checked_at"),
                "classes": ("collapse",),
            },
        ),
    )
