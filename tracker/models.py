from django.db import models
from django.contrib.auth.models import User


class Reason(models.Model):
    MOOD_TYPES = [
        ("negative", "Negative"),
        ("neutral", "Neutral"),
        ("positive", "Positive"),
    ]

    # Category for better grouping
    CATEGORY_CHOICES = [
        ("sleep", "Sleep Related"),
        ("work", "Work/School"),
        ("relationships", "Relationships"),
        ("health", "Health"),
        ("weather", "Weather/Environment"),
        ("achievement", "Achievements"),
        ("other", "Other"),
    ]

    text = models.CharField(max_length=100)
    mood_type = models.CharField(max_length=10, choices=MOOD_TYPES)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="other"
    )
    is_generic = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Action(models.Model):
    CATEGORY_CHOICES = [
        ("rest", "Rest/Sleep"),
        ("social", "Social"),
        ("activity", "Physical Activity"),
        ("mindfulness", "Mindfulness"),
        ("creative", "Creative"),
        ("other", "Other"),
    ]

    text = models.CharField(max_length=100)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="other"
    )
    reasons = models.ManyToManyField(Reason, related_name="actions", blank=True)
    is_generic = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class MoodEntry(models.Model):
    MOOD_CHOICES = [
        (1, "Very bad"),
        (2, "Bad"),
        (3, "Neutral"),
        (4, "Good"),
        (5, "Excellent"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="mood_entries"
    )
    mood = models.IntegerField(choices=MOOD_CHOICES)
    reason = models.ForeignKey(
        Reason,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mood_entries",
    )
    action = models.ForeignKey(
        Action,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mood_entries",
    )
    notes = models.TextField(blank=True)

    # Fields for tracking effectiveness
    action_worked = models.BooleanField(null=True, blank=True)
    action_checked_at = models.DateTimeField(null=True, blank=True)

    # Auto timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Helper properties for statistics
    @property
    def day_of_week(self):
        return self.created_at.strftime("%A")  # Monday, Tuesday, etc.

    @property
    def week_number(self):
        return self.created_at.isocalendar()[1]

    @property
    def month(self):
        return self.created_at.strftime("%B")  # January, February, etc.

    @property
    def hour_of_day(self):
        return self.created_at.hour

    @property
    def custom_reason_text(self):
        """Extract custom reason from notes"""
        if self.reason:
            return None
        if not self.notes:
            return None

        import re

        # Look for "Custom reason: XXXX" pattern
        match = re.search(r"Custom reason: (.*?)(\n|$)", self.notes)
        if match:
            return match.group(1)
        return None

    @property
    def custom_action_text(self):
        """Extract custom action from notes"""
        if self.action and self.action.text != "Custom action":
            return None
        if not self.notes:
            return None

        import re

        # Look for "Custom action: XXXX" pattern
        match = re.search(r"Custom action: (.*?)(\n|$)", self.notes)
        if match:
            return match.group(1)
        return None

    @property
    def display_reason(self):
        """Get reason text (either from reason or custom)"""
        if self.reason:
            return self.reason.text
        custom = self.custom_reason_text
        return custom if custom else "Custom reason"

    @property
    def display_action(self):
        """Get action text (either from action or custom)"""
        if self.action and self.action.text != "Custom action":
            return self.action.text
        custom = self.custom_action_text
        return custom if custom else "Custom action"

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["user", "mood"]),
            models.Index(fields=["created_at"]),  # For time-based queries
        ]

    def __str__(self):
        return f"{self.user} - {self.mood} - {self.created_at.date()}"
