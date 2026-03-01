from django.test import TestCase
from tracker.models import Reason, Action
from tracker.forms import (
    Step1MoodForm,
    Step2ReasonForm,
    Step3ActionForm,
    ActionFeedbackForm,
)


class FormTests(TestCase):
    """Test that forms work correctly"""

    def setUp(self):
        # Create test data
        self.positive_reason = Reason.objects.create(
            text="Beautiful sunny weather", mood_type="positive", category="weather"
        )

        self.negative_reason = Reason.objects.create(
            text="The weather is gloomy", mood_type="negative", category="weather"
        )

        self.neutral_reason = Reason.objects.create(
            text="Weather is typical", mood_type="neutral", category="weather"
        )

        self.positive_action = Action.objects.create(
            text="Write gratitude", category="mindfulness", is_generic=False
        )
        self.positive_action.reasons.add(self.positive_reason)

    def test_step1_form_valid(self):
        """Test Step 1 form with valid data"""
        form_data = {"mood": "5"}
        form = Step1MoodForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_step1_form_invalid(self):
        """Test Step 1 form with invalid data"""
        form_data = {"mood": "6"}  # Invalid mood value
        form = Step1MoodForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_step2_form_positive_mood(self):
        """Test Step 2 form shows positive reasons for mood 5"""
        form = Step2ReasonForm(mood_value=5)
        self.assertIn("reason", form.fields)
        choices = form.fields["reason"].choices
        choice_texts = [choice[1] for choice in choices]

        self.assertIn("Beautiful sunny weather", choice_texts)
        self.assertNotIn("The weather is gloomy", choice_texts)
        self.assertNotIn("Weather is typical", choice_texts)
        self.assertIn("Other (tell us more)", choice_texts)

    def test_step2_form_negative_mood(self):
        """Test Step 2 form shows negative reasons for mood 1"""
        form = Step2ReasonForm(mood_value=1)
        choices = form.fields["reason"].choices
        choice_texts = [choice[1] for choice in choices]

        self.assertIn("The weather is gloomy", choice_texts)
        self.assertNotIn("Beautiful sunny weather", choice_texts)
        self.assertNotIn("Weather is typical", choice_texts)

    def test_step2_form_neutral_mood(self):
        """Test Step 2 form shows neutral reasons for mood 3"""
        form = Step2ReasonForm(mood_value=3)
        choices = form.fields["reason"].choices
        choice_texts = [choice[1] for choice in choices]

        self.assertIn("Weather is typical", choice_texts)
        self.assertNotIn("Beautiful sunny weather", choice_texts)
        self.assertNotIn("The weather is gloomy", choice_texts)

    def test_step2_form_with_custom_queryset(self):
        """Test Step 2 form accepts custom queryset"""
        custom_reasons = [self.positive_reason]
        form = Step2ReasonForm(mood_value=5, custom_queryset=custom_reasons)
        choices = form.fields["reason"].choices
        self.assertEqual(len(choices), 2)  # 1 reason + Other option
        self.assertEqual(choices[0][1], "Beautiful sunny weather")

    def test_step3_form_for_positive_reason(self):
        """Test Step 3 form shows actions for positive reason"""
        form = Step3ActionForm(
            reason_id=self.positive_reason.id, is_custom=False, mood_value=5
        )
        self.assertIn("action", form.fields)
        label = form.fields["action"].label
        self.assertEqual(label, "What would make this excellent day even better?")

    def test_step3_form_for_negative_reason(self):
        """Test Step 3 form shows actions for negative reason"""
        form = Step3ActionForm(
            reason_id=self.negative_reason.id, is_custom=False, mood_value=1
        )
        label = form.fields["action"].label
        self.assertEqual(label, "What might help you feel a little better?")

    def test_step3_form_custom_reason(self):
        """Test Step 3 form handles custom reasons"""
        form = Step3ActionForm(reason_id=None, is_custom=True, mood_value=3)
        self.assertIn("action", form.fields)

    def test_feedback_form(self):
        """Test feedback form"""
        form = ActionFeedbackForm()
        self.assertIn("action_worked", form.fields)
        choices = form.fields["action_worked"].choices
        self.assertEqual(len(choices), 2)
        self.assertEqual(choices[0][1], "Yes, it helped!")
        self.assertEqual(choices[1][1], "No, it didn't help")
