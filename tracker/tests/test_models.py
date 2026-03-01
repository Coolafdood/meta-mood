from django.test import TestCase
from django.contrib.auth.models import User
from tracker.models import Reason, Action, MoodEntry


class ModelTests(TestCase):
    """Test that models work correctly"""

    def setUp(self):
        # Create test reasons
        self.positive_reason = Reason.objects.create(
            text="Beautiful sunny weather",
            mood_type="positive",
            category="weather",
            is_generic=False,
        )

        self.negative_reason = Reason.objects.create(
            text="The weather is gloomy",
            mood_type="negative",
            category="weather",
            is_generic=False,
        )

        # Create test actions
        self.positive_action = Action.objects.create(
            text="Write in gratitude journal", category="mindfulness", is_generic=False
        )

        self.negative_action = Action.objects.create(
            text="Take a nap", category="rest", is_generic=False
        )

        # Link actions to reasons
        self.positive_action.reasons.add(self.positive_reason)
        self.negative_action.reasons.add(self.negative_reason)

        # Create test user
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_reason_creation(self):
        """Test that reasons are created correctly"""
        self.assertEqual(Reason.objects.count(), 2)
        self.assertEqual(self.positive_reason.mood_type, "positive")
        self.assertEqual(self.negative_reason.category, "weather")
        self.assertEqual(str(self.positive_reason), "Beautiful sunny weather")

    def test_action_creation(self):
        """Test that actions are created correctly"""
        self.assertEqual(Action.objects.count(), 2)
        self.assertEqual(self.positive_action.category, "mindfulness")
        self.assertEqual(str(self.positive_action), "Write in gratitude journal")

    def test_action_reason_relationship(self):
        """Test that actions are properly linked to reasons"""
        # Positive reason should have positive action
        self.assertIn(self.positive_action, self.positive_reason.actions.all())
        # Negative reason should have negative action
        self.assertIn(self.negative_action, self.negative_reason.actions.all())
        # Positive reason should NOT have negative action
        self.assertNotIn(self.negative_action, self.positive_reason.actions.all())

    def test_mood_entry_creation(self):
        """Test that mood entries are created correctly"""
        entry = MoodEntry.objects.create(
            user=self.user,
            mood=5,
            reason=self.positive_reason,
            action=self.positive_action,
            notes="Test note",
        )

        self.assertEqual(MoodEntry.objects.count(), 1)
        self.assertEqual(entry.user, self.user)
        self.assertEqual(entry.mood, 5)
        self.assertEqual(entry.reason, self.positive_reason)
        self.assertEqual(entry.action, self.positive_action)
        self.assertEqual(entry.notes, "Test note")
        self.assertIsNone(entry.action_worked)

    def test_mood_entry_str_method(self):
        """Test the string representation of mood entry"""
        entry = MoodEntry.objects.create(
            user=self.user, mood=5, reason=self.positive_reason
        )
        expected = f"{self.user} - 5 - {entry.created_at.date()}"
        self.assertEqual(str(entry), expected)

    def test_helper_properties(self):
        """Test the helper properties for statistics"""
        from django.utils import timezone

        entry = MoodEntry.objects.create(
            user=self.user,
            mood=5,
            reason=self.positive_reason,
            created_at=timezone.now(),
        )

        # Test day_of_week property
        self.assertIn(
            entry.day_of_week,
            [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ],
        )

        # Test week_number property
        self.assertIsInstance(entry.week_number, int)

        # Test month property
        self.assertIn(
            entry.month,
            [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
            ],
        )

        # Test hour_of_day property
        self.assertIsInstance(entry.hour_of_day, int)
        self.assertGreaterEqual(entry.hour_of_day, 0)
        self.assertLessEqual(entry.hour_of_day, 23)
