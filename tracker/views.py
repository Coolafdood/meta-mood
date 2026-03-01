from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Avg, Q

import random

from .models import MoodEntry, Reason, Action
from .forms import Step1MoodForm, Step2ReasonForm, Step3ActionForm, ActionFeedbackForm


# Helper function for icons
def get_category_icon(category):
    """Return appropriate icon for each category"""
    icons = {
        "sleep": "😴",
        "work": "💼",
        "relationships": "👥",
        "health": "❤️",
        "weather": "☁️",
        "achievement": "🏆",
        "other": "📝",
    }
    return icons.get(category, "📊")


# Landing page with generic information
def index(request):
    """Landing page with generic information"""
    return render(request, "tracker/index.html")


@login_required
def step1_mood(request):
    """Step 1: User selects their mood"""
    if request.method == "POST":
        form = Step1MoodForm(request.POST)
        if form.is_valid():
            # Save mood in session
            request.session["mood"] = int(form.cleaned_data["mood"])
            return redirect("tracker:step2_reason")
    else:
        form = Step1MoodForm()

    return render(request, "tracker/step1_mood.html", {"form": form})


@login_required
def step2_reason(request):
    """Step 2: User selects reason for their mood"""
    mood = request.session.get("mood")
    if not mood:
        messages.error(request, "Please start from the beginning.")
        return redirect("tracker:step1_mood")

    # Determine mood type for filtering reasons
    if mood <= 2:
        mood_type = "negative"
    elif mood == 3:
        mood_type = "neutral"
    else:
        mood_type = "positive"

    # For GET request - preparee reasons
    if request.method == "GET":
        # Get all reasons for this mood type
        all_reasons = Reason.objects.filter(mood_type=mood_type, is_generic=False)

        # Strategy: Get up to 2 from each category
        categories = [
            "sleep",
            "work",
            "relationships",
            "health",
            "weather",
            "achievement",
            "other",
        ]
        selected_reasons = []

        for category in categories:
            if category == "other":
                # handled by form
                continue

            category_reasons = all_reasons.filter(category=category)
            count = category_reasons.count()

            if count >= 2:
                # Randomly select 2 reasons from categories with 2 or more reasons
                reason_list = list(category_reasons)
                selected_reasons.extend(random.sample(reason_list, 2))
            elif count == 1:
                # Take the only one reason if there's just one
                selected_reasons.extend(category_reasons)
            # If there are no reasons in this category, it will simply be skipped

        # Shuffle the final list for variety
        random.shuffle(selected_reasons)

        # Limit to 10-12 total
        selected_reasons = selected_reasons[:12]

        # Create custom form with these reasons
        form = Step2ReasonForm(mood_value=mood, custom_queryset=selected_reasons)

        total_options = len(selected_reasons)

    else:
        # POST request - process form submission
        form = Step2ReasonForm(request.POST, mood_value=mood)
        total_options = 0

        if form.is_valid():
            reason_id = form.cleaned_data.get("reason")
            custom_reason = form.cleaned_data.get("custom_reason")

            if reason_id == "other":
                # Save that it's a custom reason
                request.session["is_custom_reason"] = True
                request.session["custom_reason_text"] = custom_reason
            else:
                # Save the selected reason
                request.session["is_custom_reason"] = False
                request.session["reason_id"] = int(reason_id)

            return redirect("tracker:step3_action")

    return render(
        request,
        "tracker/step2_reason.html",
        {
            "form": form,
            "mood": mood,
            "total_options": total_options,
        },
    )


@login_required
def step3_action(request):
    """Step 3: User selects an action to try"""
    mood = request.session.get("mood")
    reason_id = request.session.get("reason_id")
    is_custom_reason = request.session.get("is_custom_reason", False)
    custom_reason_text = request.session.get("custom_reason_text", "")

    if not mood:
        messages.error(request, "Please start from the beginning.")
        return redirect("tracker:step1_mood")

    # For GET request - prepare smart action selection
    if request.method == "GET" and not is_custom_reason and reason_id:
        reason = Reason.objects.get(id=reason_id)

        # Get actions related to this reason
        all_actions = reason.actions.all()

        # Group actions by category
        action_categories = [
            "rest",
            "social",
            "activity",
            "mindfulness",
            "creative",
            "other",
        ]
        selected_actions = []

        for category in action_categories:
            if category == "other":
                # handled by form, always include "Other" option
                continue

            category_actions = all_actions.filter(category=category)
            count = category_actions.count()

            if count >= 2:
                # Randomly select 2 actions from categories with 2 or more actions
                action_list = list(category_actions)
                selected_actions.extend(random.sample(action_list, 2))
            elif count == 1:
                # Take the only one action if there's just one
                selected_actions.extend(category_actions)
            # If there are no actions in this category, it will simply be skipped

        # Shuffle and limit to 12 total
        random.shuffle(selected_actions)
        selected_actions = selected_actions[:12]

        # Create form with these actions
        form = Step3ActionForm(
            reason_id=reason_id,
            is_custom=is_custom_reason,
            custom_queryset=selected_actions,
            mood_value=mood,
        )

    else:
        # POST request - process form submission
        form = Step3ActionForm(
            request.POST or None,
            reason_id=reason_id,
            is_custom=is_custom_reason,
            mood_value=mood,
        )

        if request.method == "POST" and form.is_valid():
            action_id = form.cleaned_data.get("action")
            custom_action = form.cleaned_data.get("custom_action")

            # Create the mood entry
            reason = None
            if not is_custom_reason and reason_id:
                reason = Reason.objects.get(id=reason_id)

            action = None
            notes = ""

            if action_id == "custom":
                notes = f"Custom action: {custom_action}"
                if is_custom_reason:
                    notes = f"Custom reason: {custom_reason_text}\n{notes}"
                custom_action_obj, _ = Action.objects.get_or_create(
                    text="Custom action",
                    defaults={
                        "category": "other",
                        "is_generic": True
                }
                )
                action = custom_action_obj
             
            else:
                action = Action.objects.get(id=int(action_id))
                if is_custom_reason:
                    notes = f"Custom reason: {custom_reason_text}"

            mood_entry = MoodEntry.objects.create(
                user=request.user, mood=mood, reason=reason, action=action, notes=notes
            )

            # Clear session data
            for key in ["mood", "reason_id", "is_custom_reason", "custom_reason_text"]:
                if key in request.session:
                    del request.session[key]

            # Save the entry ID for feedback later
            request.session["last_mood_entry_id"] = mood_entry.id

            messages.success(request, "Your mood has been recorded!")
            return redirect("tracker:dashboard")

    context = {
        "form": form,
        "mood": mood,
        "is_custom_reason": is_custom_reason,
        "custom_reason_text": custom_reason_text if is_custom_reason else None,
    }
    return render(request, "tracker/step3_action.html", context)


# Dashboard view
@login_required
def dashboard(request):
    """Enhanced dashboard with category statistics"""
    # Get all entries for the user
    entries = MoodEntry.objects.filter(user=request.user).select_related(
        "reason", "action"
    )
    total_entries = entries.count()

    # Get statistics by category (only if there are entries)
    category_stats = []
    if total_entries > 0:
        # Get all categories that have at least 1 entry
        categories_with_data = (
            entries.exclude(reason__isnull=True)
            .values("reason__category")
            .annotate(total_entries=Count("id"))
            .filter(total_entries__gte=1)
        )

        for cat in categories_with_data:
            category = cat["reason__category"]
            category_entries = entries.filter(reason__category=category)

            # Get reasons within this category
            reasons_stats = (
                category_entries.values("reason__text", "reason__mood_type")
                .annotate(count=Count("id"), avg_mood=Avg("mood"))
                .order_by("-count")[:3]
            )

            # Overall category stats
            overall = category_entries.aggregate(
                avg_mood=Avg("mood"),
                total=Count("id"),
                positive_count=Count("id", filter=Q(mood__gte=4)),
            )

            positive_percentage = (
                (overall["positive_count"] / overall["total"] * 100)
                if overall["total"] > 0
                else 0
            )

            category_stats.append(
                {
                    "name": category,
                    "display_name": dict(Reason.CATEGORY_CHOICES).get(
                        category, category
                    ),
                    "total_entries": overall["total"],
                    "avg_mood": (
                        round(overall["avg_mood"], 1) if overall["avg_mood"] else 0
                    ),
                    "positive_percentage": round(positive_percentage, 1),
                    "top_reasons": reasons_stats,
                    "icon": get_category_icon(category),
                    "avg_mood_percentage": (
                        round((overall["avg_mood"] / 5) * 100, 1)
                        if overall["avg_mood"]
                        else 0
                    ),
                }
            )

        # Sort categories by number of entries (most active first)
        category_stats.sort(key=lambda x: x["total_entries"], reverse=True)

    # Get recent entries
    recent_entries = entries[:5]

    # Calculate overall average mood
    overall_avg = entries.aggregate(Avg("mood"))["mood__avg"]

    # Original statistics
    if total_entries > 0:
        mood_distribution = (
            entries.values("mood").annotate(count=Count("mood")).order_by("mood")
        )
        actions_feedback = (
            entries.exclude(action_worked__isnull=True)
            .values("action__text")
            .annotate(count=Count("id"), success_rate=Avg("action_worked") * 100)
            .order_by("-success_rate")
        )
    else:
        mood_distribution = []
        actions_feedback = []

    # ============ FIXED FEEDBACK LOGIC ============
    # Time threshold (20 seconds for testing)
    time_threshold_seconds = 20
    
    # Look for entries that need feedback
    pending_feedback = MoodEntry.objects.filter(
        user=request.user,
        action__isnull=False,
        action_worked__isnull=True,
    ).order_by('created_at')
    
    # Create feedback forms for eligible entries
    feedback_forms = []
    for candidate in pending_feedback:
        time_passed = timezone.now() - candidate.created_at
        if time_passed.total_seconds() > time_threshold_seconds:
            form = ActionFeedbackForm(initial={"entry_id": candidate.id})
            feedback_forms.append({"entry": candidate, "form": form})
            if len(feedback_forms) >= 3:  # Limit to 3
                break
    
    has_feedback_pending = len(feedback_forms) > 0

    context = {
        # New enhanced stats
        "category_stats": category_stats,
        "overall_avg_mood": round(overall_avg, 1) if overall_avg else 0,
        # Original stats
        "entries": recent_entries,
        "recent_entries": recent_entries,
        "total_entries": total_entries,
        "avg_mood": round(overall_avg, 1) if overall_avg else 0,
        "mood_distribution": mood_distribution,
        "actions_feedback": actions_feedback,
        # NEW: Multiple feedback forms
        "feedback_forms": feedback_forms,
        "has_feedback_pending": has_feedback_pending,
        # New helpful flags
        "is_new_user": total_entries < 3,
    }

    return render(request, "tracker/dashboard.html", context)


@login_required
def submit_feedback(request, entry_id):
    """Submit feedback on whether an action worked"""
    entry = get_object_or_404(MoodEntry, id=entry_id, user=request.user)

    # Prevent multiple feedback submissions
    if entry.action_worked is not None:
        messages.warning(request, "Feedback already submitted for this entry.")
        return redirect("tracker:dashboard")

    if request.method == "POST":
        form = ActionFeedbackForm(request.POST)
        if form.is_valid():
            # Convert string 'True'/'False' to boolean
            worked_value = form.cleaned_data["action_worked"]
            entry.action_worked = worked_value == "True" or worked_value is True
            entry.action_checked_at = timezone.now()
            entry.save()

            # Clear the session
            if "last_mood_entry_id" in request.session:
                del request.session["last_mood_entry_id"]

            messages.success(request, "Thank you for your feedback!")

    return redirect("tracker:dashboard")


@login_required
def delete_entry(request, entry_id):
    """Delete a mood entry"""
    entry = get_object_or_404(MoodEntry, id=entry_id, user=request.user)
    if request.method == "POST":
        entry.delete()
        messages.success(request, "Entry deleted successfully.")
    return redirect("tracker:dashboard")
