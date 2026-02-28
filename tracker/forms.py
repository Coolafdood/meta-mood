from django import forms
from .models import MoodEntry, Reason, Action


class Step1MoodForm(forms.Form):
    mood = forms.ChoiceField(
        choices=MoodEntry.MOOD_CHOICES,
        widget=forms.RadioSelect,
        label="How are you feeling today?"
    )


class Step2ReasonForm(forms.Form):
    def __init__(self, *args, **kwargs):
        mood_value = kwargs.pop('mood_value', None)
        super().__init__(*args, **kwargs)
        
        # Determine mood type based on mood value
        if mood_value:
            if mood_value <= 2:
                mood_type = "negative"
            elif mood_value == 3:
                mood_type = "neutral"
            else:
                mood_type = "positive"
            
            # Filter reasons based on mood type and add "Other" option
            reasons = Reason.objects.filter(mood_type=mood_type)
            choices = [(r.id, r.text) for r in reasons]
            choices.append(('other', 'Other (tell us more)'))
            
            self.fields['reason'] = forms.ChoiceField(
                choices=choices,
                widget=forms.RadioSelect,
                label="Why do you feel this way?"
            )
            
            self.fields['custom_reason'] = forms.CharField(
                widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Please tell us more...'}),
                required=False,
                label="Your reason"
            )


class Step3ActionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        reason_id = kwargs.pop('reason_id', None)
        is_custom = kwargs.pop('is_custom', False)
        super().__init__(*args, **kwargs)
        
        if is_custom:
            # Show generic actions for custom reasons
            actions = Action.objects.filter(is_generic=True)
        else:
            # Show actions related to the selected reason
            try:
                reason = Reason.objects.get(id=reason_id)
                actions = reason.actions.all()
                if not actions.exists():
                    actions = Action.objects.filter(is_generic=True)
            except Reason.DoesNotExist:
                actions = Action.objects.filter(is_generic=True)
        
        choices = [(a.id, a.text) for a in actions]
        choices.append(('custom', 'Something else'))
        
        self.fields['action'] = forms.ChoiceField(
            choices=choices,
            widget=forms.RadioSelect,
            label="What might help you feel better?"
        )
        
        self.fields['custom_action'] = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder': 'What would you like to try?'}),
            required=False,
            label="Your action"
        )


class ActionFeedbackForm(forms.Form):
    action_worked = forms.ChoiceField(
        choices=[(True, 'Yes, it helped!'), (False, 'No, it didn\'t help')],
        widget=forms.RadioSelect,
        label="Did the action help you?"
    )