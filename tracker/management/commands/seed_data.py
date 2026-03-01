from django.core.management.base import BaseCommand
from tracker.models import Reason, Action


class Command(BaseCommand):
    help = "Safely seed the database with initial reasons and actions"

    def handle(self, *args, **options):
        self.stdout.write("Starting safe database seeding...")
        self.stdout.write("   (This will not delete existing data)\n")

        # ============ CREATE/UPDATE REASONS ============
        self.stdout.write(" Creating/updating reasons...")

        reasons_data = [
            # Sleep category
            {
                "text": "I didn't sleep well",
                "mood_type": "negative",
                "category": "sleep",
            },
            {
                "text": "I had trouble falling asleep",
                "mood_type": "negative",
                "category": "sleep",
            },
            {
                "text": "I woke up too early",
                "mood_type": "negative",
                "category": "sleep",
            },
            {
                "text": "I slept really well",
                "mood_type": "positive",
                "category": "sleep",
            },
            {
                "text": "I had a refreshing sleep",
                "mood_type": "positive",
                "category": "sleep",
            },
            {"text": "I slept okay", "mood_type": "neutral", "category": "sleep"},
            # Weather category
            {
                "text": "Beautiful sunny weather",
                "mood_type": "positive",
                "category": "weather",
            },
            {
                "text": "Perfect temperature outside",
                "mood_type": "positive",
                "category": "weather",
            },
            {
                "text": "The weather is gloomy",
                "mood_type": "negative",
                "category": "weather",
            },
            {
                "text": "It's too hot outside",
                "mood_type": "negative",
                "category": "weather",
            },
            {
                "text": "Rainy day making me cozy",
                "mood_type": "positive",
                "category": "weather",
            },
            {
                "text": "Rainy day making me sad",
                "mood_type": "negative",
                "category": "weather",
            },
            {
                "text": "Weather is typical",
                "mood_type": "neutral",
                "category": "weather",
            },
            # Work category
            {
                "text": "Stressed about work",
                "mood_type": "negative",
                "category": "work",
            },
            {
                "text": "Finished a big project",
                "mood_type": "positive",
                "category": "work",
            },
            {
                "text": "Got recognition at work",
                "mood_type": "positive",
                "category": "work",
            },
            {"text": "Too much workload", "mood_type": "negative", "category": "work"},
            {"text": "Regular work day", "mood_type": "neutral", "category": "work"},
            # Relationships category
            {
                "text": "Great time with friends",
                "mood_type": "positive",
                "category": "relationships",
            },
            {
                "text": "Argument with partner",
                "mood_type": "negative",
                "category": "relationships",
            },
            {
                "text": "Feeling lonely",
                "mood_type": "negative",
                "category": "relationships",
            },
            {
                "text": "Quality time with family",
                "mood_type": "positive",
                "category": "relationships",
            },
            # Health category
            {"text": "Feeling sick", "mood_type": "negative", "category": "health"},
            {
                "text": "Feeling healthy and energetic",
                "mood_type": "positive",
                "category": "health",
            },
            {
                "text": "Good workout today",
                "mood_type": "positive",
                "category": "health",
            },
            {"text": "Physical pain", "mood_type": "negative", "category": "health"},
            # Achievement category
            {
                "text": "Achieved a goal",
                "mood_type": "positive",
                "category": "achievement",
            },
            {
                "text": "Learned something new",
                "mood_type": "positive",
                "category": "achievement",
            },
            {
                "text": "Made progress on project",
                "mood_type": "positive",
                "category": "achievement",
            },
            # Generic/Other
            {
                "text": "Other reason",
                "mood_type": "neutral",
                "category": "other",
                "is_generic": True,
            },
        ]

        for reason_data in reasons_data:
            reason, created = Reason.objects.get_or_create(
                text=reason_data["text"],  # Find by unique text
                defaults={  # Only used if creating new
                    "mood_type": reason_data["mood_type"],
                    "category": reason_data["category"],
                    "is_generic": reason_data.get("is_generic", False),
                },
            )
            if created:
                self.stdout.write(f"Created reason: {reason.text}")
            else:
                # Optionally update existing reasons if needed
                needs_update = False
                if reason.mood_type != reason_data["mood_type"]:
                    reason.mood_type = reason_data["mood_type"]
                    needs_update = True
                if reason.category != reason_data["category"]:
                    reason.category = reason_data["category"]
                    needs_update = True
                if reason.is_generic != reason_data.get("is_generic", False):
                    reason.is_generic = reason_data.get("is_generic", False)
                    needs_update = True

                if needs_update:
                    reason.save()
                    self.stdout.write(f"Updated reason: {reason.text}")
                else:
                    self.stdout.write(f"Already exists: {reason.text}")

        # Get reasons by mood type for later connections
        positive_reasons = Reason.objects.filter(mood_type="positive")
        negative_reasons = Reason.objects.filter(mood_type="negative")
        neutral_reasons = Reason.objects.filter(mood_type="neutral")

        self.stdout.write(f"\n Reasons summary:")
        self.stdout.write(f"   Positive: {positive_reasons.count()}")
        self.stdout.write(f"   Negative: {negative_reasons.count()}")
        self.stdout.write(f"   Neutral: {neutral_reasons.count()}")

        # ============ CREATE/UPDATE ACTIONS ============
        self.stdout.write("\n Creating/updating actions by mood type...")

        # 1. ACTIONS FOR POSITIVE MOODS (4-5) - Enhance/Maintain
        positive_actions = [
            # Mindfulness/Reflection
            {
                "text": "Write down 3 things you're grateful for",
                "category": "mindfulness",
            },
            {"text": "Savor this good moment", "category": "mindfulness"},
            {"text": "Take a photo of something beautiful", "category": "creative"},
            # Social
            {"text": "Share your good mood with someone", "category": "social"},
            {"text": "Help someone else feel good too", "category": "social"},
            {"text": "Do a random act of kindness", "category": "social"},
            # Creative/Fun
            {"text": "Do something you're passionate about", "category": "creative"},
            {"text": "Plan something fun for the weekend", "category": "creative"},
            {"text": "Dance to your favorite song", "category": "activity"},
            {"text": "Celebrate your good mood", "category": "social"},
        ]

        positive_action_objects = []
        for action_data in positive_actions:
            action, created = Action.objects.get_or_create(
                text=action_data["text"],
                defaults={"category": action_data["category"], "is_generic": False},
            )
            positive_action_objects.append(action)
            if created:
                self.stdout.write(f"  Created positive action: {action.text}")
            else:
                self.stdout.write(f"  Already exists: {action.text}")

        # 2. ACTIONS FOR NEGATIVE MOODS (1-2) - Improve/Fix
        negative_actions = [
            # Rest/Sleep
            {"text": "Take a short nap", "category": "rest"},
            {"text": "Go to bed earlier", "category": "rest"},
            {"text": "Create a relaxing bedtime routine", "category": "rest"},
            {"text": "Use white noise or calming music", "category": "rest"},
            # Mindfulness
            {
                "text": "Practice deep breathing for 5 minutes",
                "category": "mindfulness",
            },
            {"text": "Try meditation for 5 minutes", "category": "mindfulness"},
            {"text": "Write down what's bothering you", "category": "mindfulness"},
            # Activity
            {"text": "Go for a walk outside", "category": "activity"},
            {"text": "Do some gentle stretching", "category": "activity"},
            {"text": "Exercise for 15 minutes", "category": "activity"},
            # Social
            {"text": "Talk to a friend or family member", "category": "social"},
            {"text": "Call someone who cares about you", "category": "social"},
            # Comfort
            {"text": "Listen to calming music", "category": "creative"},
            {"text": "Make yourself a cup of tea", "category": "rest"},
            {"text": "Take a warm shower or bath", "category": "rest"},
            {"text": "Watch something funny", "category": "creative"},
            {"text": "Give yourself permission to rest", "category": "rest"},
        ]

        negative_action_objects = []
        for action_data in negative_actions:
            action, created = Action.objects.get_or_create(
                text=action_data["text"],
                defaults={"category": action_data["category"], "is_generic": False},
            )
            negative_action_objects.append(action)
            if created:
                self.stdout.write(f"  ✅ Created negative action: {action.text}")
            else:
                self.stdout.write(f"  ⏩ Already exists: {action.text}")

        # 3. ACTIONS FOR NEUTRAL MOODS (3) - Balanced
        neutral_actions = [
            {"text": "Check in with how you're feeling", "category": "mindfulness"},
            {"text": "Do something small you enjoy", "category": "creative"},
            {"text": "Connect with someone briefly", "category": "social"},
            {"text": "Go for a short walk", "category": "activity"},
            {"text": "Read a few pages of a book", "category": "creative"},
            {"text": "Listen to a podcast", "category": "creative"},
            {"text": "Tidy up one small area", "category": "activity"},
            {"text": "Plan something for tomorrow", "category": "mindfulness"},
        ]

        neutral_action_objects = []
        for action_data in neutral_actions:
            action, created = Action.objects.get_or_create(
                text=action_data["text"],
                defaults={"category": action_data["category"], "is_generic": False},
            )
            neutral_action_objects.append(action)
            if created:
                self.stdout.write(f"  Created neutral action: {action.text}")
            else:
                self.stdout.write(f"  Already exists: {action.text}")

        # 4. GENERIC ACTIONS (for 'Other' reasons)
        generic_actions = [
            # Positive generic
            {
                "text": "Savor this moment",
                "category": "mindfulness",
                "mood": "positive",
            },
            {
                "text": "Share your positive energy",
                "category": "social",
                "mood": "positive",
            },
            # Negative generic
            {
                "text": "Be kind to yourself",
                "category": "mindfulness",
                "mood": "negative",
            },
            {
                "text": "Remember this feeling will pass",
                "category": "mindfulness",
                "mood": "negative",
            },
            # Neutral generic
            {
                "text": "Take a moment for yourself",
                "category": "mindfulness",
                "mood": "neutral",
            },
            {
                "text": "Do one small thing today",
                "category": "creative",
                "mood": "neutral",
            },
            # Truly generic (for all moods)
            {"text": "Take time for yourself", "category": "other", "mood": "all"},
            {"text": "Do something you enjoy", "category": "other", "mood": "all"},
            {"text": "Change your environment", "category": "other", "mood": "all"},
            {"text": "Talk to someone", "category": "social", "mood": "all"},
        ]

        for action_data in generic_actions:
            action, created = Action.objects.get_or_create(
                text=action_data["text"],
                defaults={"category": action_data["category"], "is_generic": True},
            )
            if created:
                self.stdout.write(f"  Created generic action: {action.text}")
            else:
                self.stdout.write(f"  Already exists: {action.text}")

        # ============ CONNECT ACTIONS TO REASONS ============
        self.stdout.write("\n Connecting actions to reasons...")

        # Clear existing connections and reconnect (safe operation)
        # This ensures relationships are correct even if they changed

        # Connect positive actions to ALL positive reasons
        for action in positive_action_objects:
            action.reasons.clear()
            action.reasons.add(*positive_reasons)
            self.stdout.write(
                f"   Connected '{action.text}' to {positive_reasons.count()} positive reasons"
            )

        # Connect negative actions to ALL negative reasons
        for action in negative_action_objects:
            action.reasons.clear()
            action.reasons.add(*negative_reasons)
            self.stdout.write(
                f"   Connected '{action.text}' to {negative_reasons.count()} negative reasons"
            )

        # Connect neutral actions to ALL neutral reasons
        for action in neutral_action_objects:
            action.reasons.clear()
            action.reasons.add(*neutral_reasons)
            self.stdout.write(
                f"   Connected '{action.text}' to {neutral_reasons.count()} neutral reasons"
            )

        # Connect generic actions based on their mood
        generic_positive = Action.objects.filter(
            text__in=[
                a["text"] for a in generic_actions if a.get("mood") == "positive"
            ],
            is_generic=True,
        )
        for action in generic_positive:
            action.reasons.clear()
            action.reasons.add(*positive_reasons)

        generic_negative = Action.objects.filter(
            text__in=[
                a["text"] for a in generic_actions if a.get("mood") == "negative"
            ],
            is_generic=True,
        )
        for action in generic_negative:
            action.reasons.clear()
            action.reasons.add(*negative_reasons)

        generic_neutral = Action.objects.filter(
            text__in=[a["text"] for a in generic_actions if a.get("mood") == "neutral"],
            is_generic=True,
        )
        for action in generic_neutral:
            action.reasons.clear()
            action.reasons.add(*neutral_reasons)

        # Truly generic actions (mood="all") connect to all reasons
        generic_all = Action.objects.filter(
            text__in=[a["text"] for a in generic_actions if a.get("mood") == "all"],
            is_generic=True,
        )
        for action in generic_all:
            action.reasons.clear()
            action.reasons.add(*positive_reasons, *negative_reasons, *neutral_reasons)

        # ============ FINAL SUMMARY ============
        self.stdout.write(
            self.style.SUCCESS(
                f"\n SUCCESS! Database seeding completed:"
                f"\n    Reasons: {Reason.objects.count()} total"
                f"\n    Actions: {Action.objects.count()} total"
                f"\n"
                f"\n   Positive actions: {len(positive_action_objects)}"
                f"\n   Negative actions: {len(negative_action_objects)}"
                f"\n   Neutral actions: {len(neutral_action_objects)}"
                f"\n   Generic actions: {Action.objects.filter(is_generic=True).count()}"
            )
        )
