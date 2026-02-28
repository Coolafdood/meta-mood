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
        custom_queryset = kwargs.pop('custom_queryset', None)

        super().__init__(*args, **kwargs)
        
        # Build the form dynamically based on mood value
        if mood_value:
            if mood_value <= 2:
                mood_type = "negative"
            elif mood_value == 3:
                mood_type = "neutral"
            else:
                mood_type = "positive"
            
            # Use custom queryset if provided(for GET), otherwise get all(for POST)
            if custom_queryset is not None:
                reasons = custom_queryset
            else:
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
        # Extract additional parameters passed from the view
        reason_id = kwargs.pop('reason_id', None)
        is_custom = kwargs.pop('is_custom', False)
        custom_queryset = kwargs.pop('custom_queryset', None)
        mood_value = kwargs.pop('mood_value', None)

        # Call the parent constructor to initialize the form
        super().__init__(*args, **kwargs)
        
        # Determine action label based on mood value
        if mood_value == 1:
            action_label = "What might help you feel a little better?"
        elif mood_value == 2:
            action_label = "What could improve your mood?"
        elif mood_value == 3:
            action_label = "What would you like to do today?"
        elif mood_value == 4:
            action_label = "How would you like to enjoy this moment?"
        elif mood_value == 5:
            action_label = "What would make this excellent day even better?"
        else:
            action_label = "What would you like to do?"

        # Determine which actions to show based on reason
        if custom_queryset is not None:
            # Use custom queryset if provided (for GET with selection)
            actions = custom_queryset
        elif is_custom:
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
        
        # Build choices for the form
        choices = [(a.id, a.text) for a in actions]
        choices.append(('custom', 'Something else'))
        
        self.fields['action'] = forms.ChoiceField(
            choices=choices,
            widget=forms.RadioSelect,
            label=action_label
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
