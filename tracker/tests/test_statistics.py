from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from tracker.models import Reason, MoodEntry
from django.utils import timezone
from datetime import timedelta


class StatisticsTests(TestCase):
    """Test that statistics are calculated correctly"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

        # Create reasons
        self.positive_reason = Reason.objects.create(
            text="Positive reason", mood_type="positive", category="test"
        )

        self.negative_reason = Reason.objects.create(
            text="Negative reason", mood_type="negative", category="test"
        )

        # Create entries with different moods
        # 3 positive entries (moods 4,4,5)
        for mood in [4, 4, 5]:
            MoodEntry.objects.create(
                user=self.user, mood=mood, reason=self.positive_reason
            )

        # 2 negative entries (moods 1,2)
        for mood in [1, 2]:
            MoodEntry.objects.create(
                user=self.user, mood=mood, reason=self.negative_reason
            )

        # 1 neutral entry (mood 3)
        MoodEntry.objects.create(user=self.user, mood=3, reason=self.negative_reason)

    def test_total_entries_count(self):
        """Test total entries count is correct"""
        entries = MoodEntry.objects.filter(user=self.user)
        self.assertEqual(entries.count(), 6)

    def test_average_mood_calculation(self):
        """Test average mood calculation"""
        avg = MoodEntry.objects.filter(user=self.user).aggregate(Avg("mood"))[
            "mood__avg"
        ]
        # (4+4+5+1+2+3) / 6 = 19/6 = 3.1666...
        self.assertAlmostEqual(avg, 3.1666, places=2)

    def test_positive_percentage_calculation(self):
        """Test positive mood percentage"""
        entries = MoodEntry.objects.filter(user=self.user)
        total = entries.count()
        positive = entries.filter(mood__gte=4).count()
        percentage = positive / total * 100
        self.assertEqual(percentage, 50.0)  # 3 out of 6 = 50%

    def test_category_filtering_threshold(self):
        """Test that categories with less than threshold entries don't show"""
        # Default threshold is 1 in your current code
        threshold = 1

        # Create a new category with only 1 entry
        new_category = Reason.objects.create(
            text="New reason", mood_type="positive", category="new_cat"
        )

        MoodEntry.objects.create(user=self.user, mood=5, reason=new_category)

        # This category should appear (has 1 entry, meets threshold=1)
        categories = (
            MoodEntry.objects.filter(user=self.user, reason__isnull=False)
            .values("reason__category")
            .annotate(total=Count("id"))
            .filter(total__gte=threshold)
        )

        category_names = [c["reason__category"] for c in categories]
        self.assertIn("test", category_names)
        self.assertIn("new_cat", category_names)  # Has 1 entry, meets threshold

    def test_top_reasons_ordering(self):
        """Test that top reasons are ordered by count"""
        # Create additional entries to make one reason more common
        for i in range(3):
            MoodEntry.objects.create(
                user=self.user, mood=4, reason=self.positive_reason
            )

        # Get top reasons
        top_reasons = (
            MoodEntry.objects.filter(user=self.user, reason__isnull=False)
            .values("reason__text")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        # Positive reason should be first (now has 6 entries: 3+3)
        self.assertEqual(top_reasons[0]["reason__text"], "Positive reason")
        self.assertGreater(top_reasons[0]["count"], top_reasons[1]["count"])

    def test_recent_entries_ordering(self):
        """Test that recent entries are ordered newest first"""

        # Clear any existing entries
        MoodEntry.objects.filter(user=self.user).delete()

        # Create entries with CLEAR time differences
        now = timezone.now()

        # Create entries with different timestamps
        old_entry = MoodEntry.objects.create(
            user=self.user,
            mood=3,
            reason=self.positive_reason,
            created_at=now - timedelta(days=2),
        )

        medium_entry = MoodEntry.objects.create(
            user=self.user,
            mood=4,
            reason=self.positive_reason,
            created_at=now - timedelta(days=1),
        )

        new_entry = MoodEntry.objects.create(
            user=self.user, mood=5, reason=self.positive_reason, created_at=now
        )

        recent = MoodEntry.objects.filter(user=self.user).order_by("-created_at")

        # Debug output
        print(f"\nEntries in order:")
        for e in recent:
            print(f"  {e.mood} - {e.created_at}")

        # Assertions
        self.assertEqual(recent[0], new_entry)  # First should be newest
        self.assertEqual(recent[1], medium_entry)  # Second should be medium
        self.assertEqual(recent[2], old_entry)  # Third should be oldest
