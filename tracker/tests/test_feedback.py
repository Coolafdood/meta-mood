from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from tracker.models import Reason, Action, MoodEntry


class FeedbackTests(TestCase):
    """Test feedback functionality"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

        self.reason = Reason.objects.create(
            text="Test reason", mood_type="neutral", category="test"
        )
        self.action = Action.objects.create(text="Test action", category="test")
        self.action.reasons.add(self.reason)

    def test_feedback_not_shown_immediately(self):
        """Test feedback form doesn't show right after entry"""
        # Create entry
        entry = MoodEntry.objects.create(
            user=self.user, mood=3, reason=self.reason, action=self.action
        )

        # Set session
        session = self.client.session
        session["last_mood_entry_id"] = entry.id
        session.save()

        # Check dashboard - feedback should NOT show
        response = self.client.get(reverse("tracker:dashboard"))
        self.assertNotContains(response, "Time for a Check-in")
        self.assertNotContains(response, "Did this action help you feel better?")

    def test_feedback_submission_yes(self):
        """Test submitting 'yes' feedback works"""
        entry = MoodEntry.objects.create(
            user=self.user,
            mood=3,
            reason=self.reason,
            action=self.action,
            action_worked=None,
        )

        # Submit feedback
        response = self.client.post(
            reverse("tracker:submit_feedback", args=[entry.id]),
            {"action_worked": "True"},
        )

        # Check redirect
        self.assertRedirects(response, reverse("tracker:dashboard"))

        # Check entry was updated
        entry.refresh_from_db()
        self.assertTrue(entry.action_worked)
        self.assertIsNotNone(entry.action_checked_at)

        # Check session was cleared
        self.assertNotIn("last_mood_entry_id", self.client.session)

    def test_feedback_submission_no(self):
        """Test submitting 'no' feedback works"""
        entry = MoodEntry.objects.create(
            user=self.user,
            mood=3,
            reason=self.reason,
            action=self.action,
            action_worked=None,
        )

        # Submit feedback
        response = self.client.post(
            reverse("tracker:submit_feedback", args=[entry.id]),
            {"action_worked": "False"},
        )

        # Check entry was updated
        entry.refresh_from_db()
        self.assertFalse(entry.action_worked)

    def test_feedback_only_once(self):
        """Test feedback can only be submitted once"""
        entry = MoodEntry.objects.create(
            user=self.user,
            mood=3,
            reason=self.reason,
            action=self.action,
            action_worked=True,  # Already has feedback
        )

        # Try to submit again
        response = self.client.post(
            reverse("tracker:submit_feedback", args=[entry.id]),
            {"action_worked": "False"},
        )

        # Should still redirect
        self.assertRedirects(response, reverse("tracker:dashboard"))

        # But entry should NOT change
        entry.refresh_from_db()
        self.assertTrue(entry.action_worked)  # Still True

    def test_feedback_wrong_user(self):
        """Test users can't give feedback on others' entries"""
        other_user = User.objects.create_user(
            username="otheruser", password="otherpass123"
        )

        entry = MoodEntry.objects.create(
            user=other_user,  # Different user
            mood=3,
            reason=self.reason,
            action=self.action,
        )

        # Try to submit feedback
        response = self.client.post(
            reverse("tracker:submit_feedback", args=[entry.id]),
            {"action_worked": "True"},
        )

        # Should get 404
        self.assertEqual(response.status_code, 404)

    def test_delete_entry(self):
        """Test deleting an entry works"""
        entry = MoodEntry.objects.create(
            user=self.user, mood=3, reason=self.reason, action=self.action
        )

        self.assertEqual(MoodEntry.objects.count(), 1)

        # Delete entry
        response = self.client.post(reverse("tracker:delete_entry", args=[entry.id]))

        self.assertRedirects(response, reverse("tracker:dashboard"))
        self.assertEqual(MoodEntry.objects.count(), 0)

    def test_delete_entry_wrong_user(self):
        """Test users can't delete others' entries"""
        other_user = User.objects.create_user(
            username="otheruser", password="otherpass123"
        )

        entry = MoodEntry.objects.create(
            user=other_user, mood=3, reason=self.reason, action=self.action
        )

        response = self.client.post(reverse("tracker:delete_entry", args=[entry.id]))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(MoodEntry.objects.count(), 1)
