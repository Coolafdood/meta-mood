from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from tracker.models import Reason, Action, MoodEntry


class ViewTests(TestCase):
    """Test that views work correctly"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

        # Create test data
        self.reason = Reason.objects.create(
            text="Test reason", mood_type="positive", category="test"
        )

        self.action = Action.objects.create(text="Test action", category="test")
        self.action.reasons.add(self.reason)

    def test_index_view(self):
        """Test landing page loads"""
        response = self.client.get(reverse("tracker:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tracker/index.html")

    def test_index_view_anonymous(self):
        """Test landing page works for anonymous users"""
        self.client.logout()
        response = self.client.get(reverse("tracker:index"))
        self.assertEqual(response.status_code, 200)

    def test_step1_view_get(self):
        """Test step 1 page loads via GET"""
        response = self.client.get(reverse("tracker:step1_mood"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tracker/step1_mood.html")
        self.assertContains(response, "How are you feeling?")

    def test_step1_view_post(self):
        """Test step 1 form submission"""
        response = self.client.post(reverse("tracker:step1_mood"), {"mood": "5"})
        self.assertRedirects(response, reverse("tracker:step2_reason"))

        # Check session was set
        self.assertEqual(self.client.session.get("mood"), 5)

    def test_step2_view_redirect_if_no_mood(self):
        """Test step 2 redirects if no mood in session"""
        response = self.client.get(reverse("tracker:step2_reason"))
        self.assertRedirects(response, reverse("tracker:step1_mood"))

    def test_step2_view_with_mood(self):
        """Test step 2 loads with mood in session"""
        session = self.client.session
        session["mood"] = 5
        session.save()

        response = self.client.get(reverse("tracker:step2_reason"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tracker/step2_reason.html")

    def test_step2_view_post_reason(self):
        """Test step 2 form submission with reason"""
        session = self.client.session
        session["mood"] = 5
        session.save()

        response = self.client.post(
            reverse("tracker:step2_reason"),
            {"reason": self.reason.id, "custom_reason": ""},
        )
        self.assertRedirects(response, reverse("tracker:step3_action"))

        # Check session was updated
        self.assertEqual(self.client.session.get("reason_id"), self.reason.id)
        self.assertFalse(self.client.session.get("is_custom_reason"))

    def test_step2_view_post_custom(self):
        """Test step 2 form submission with custom reason"""
        session = self.client.session
        session["mood"] = 5
        session.save()

        response = self.client.post(
            reverse("tracker:step2_reason"),
            {"reason": "other", "custom_reason": "My custom reason"},
        )
        self.assertRedirects(response, reverse("tracker:step3_action"))

        # Check session was updated
        self.assertTrue(self.client.session.get("is_custom_reason"))
        self.assertEqual(
            self.client.session.get("custom_reason_text"), "My custom reason"
        )

    def test_step3_view_with_valid_data(self):
        """Test complete flow through step 3"""
        # Set up session
        session = self.client.session
        session["mood"] = 5
        session["reason_id"] = self.reason.id
        session["is_custom_reason"] = False
        session.save()

        # Get step 3
        response = self.client.get(reverse("tracker:step3_action"))
        self.assertEqual(response.status_code, 200)

        # Post action
        response = self.client.post(
            reverse("tracker:step3_action"),
            {"action": self.action.id, "custom_action": ""},
        )
        self.assertRedirects(response, reverse("tracker:dashboard"))

        # Check entry was created
        self.assertEqual(MoodEntry.objects.count(), 1)
        entry = MoodEntry.objects.first()
        self.assertEqual(entry.mood, 5)
        self.assertEqual(entry.reason, self.reason)
        self.assertEqual(entry.action, self.action)
