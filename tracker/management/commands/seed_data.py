from django.core.management.base import BaseCommand
from tracker.models import Reason, Action


class Command(BaseCommand):
    help = 'Seed the database with initial reasons and actions'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
   
        # Clear existing data (BE CAREFUL - only in development!)
        self.stdout.write('Clearing existing data...')
        Reason.objects.all().delete()
        Action.objects.all().delete()
   
        # Create reasons by category and mood type
        reasons_data = [
            # Sleep category
            {"text": "I didn't sleep well", "mood_type": "negative", "category": "sleep"},
            {"text": "I had trouble falling asleep", "mood_type": "negative", "category": "sleep"},
            {"text": "I woke up too early", "mood_type": "negative", "category": "sleep"},
            {"text": "I slept really well", "mood_type": "positive", "category": "sleep"},
            {"text": "I had a refreshing sleep", "mood_type": "positive", "category": "sleep"},
            {"text": "I slept okay", "mood_type": "neutral", "category": "sleep"},
   
            # Weather category
            {"text": "Beautiful sunny weather", "mood_type": "positive", "category": "weather"},
            {"text": "Perfect temperature outside", "mood_type": "positive", "category": "weather"},
            {"text": "The weather is gloomy", "mood_type": "negative", "category": "weather"},
            {"text": "It's too hot outside", "mood_type": "negative", "category": "weather"},
            {"text": "Rainy day making me cozy", "mood_type": "positive", "category": "weather"},
            {"text": "Rainy day making me sad", "mood_type": "negative", "category": "weather"},
            {"text": "Weather is typical", "mood_type": "neutral", "category": "weather"},

            # Work category
            {"text": "Stressed about work", "mood_type": "negative", "category": "work"},
            {"text": "Finished a big project", "mood_type": "positive", "category": "work"},
            {"text": "Got recognition at work", "mood_type": "positive", "category": "work"},
            {"text": "Too much workload", "mood_type": "negative", "category": "work"},
            {"text": "Regular work day", "mood_type": "neutral", "category": "work"},

            # Relationships category
            {"text": "Great time with friends", "mood_type": "positive", "category": "relationships"},
            {"text": "Argument with partner", "mood_type": "negative", "category": "relationships"},
            {"text": "Feeling lonely", "mood_type": "negative", "category": "relationships"},
            {"text": "Quality time with family", "mood_type": "positive", "category": "relationships"},

            # Health category
            {"text": "Feeling sick", "mood_type": "negative", "category": "health"},
            {"text": "Feeling healthy and energetic", "mood_type": "positive", "category": "health"},
            {"text": "Good workout today", "mood_type": "positive", "category": "health"},
            {"text": "Physical pain", "mood_type": "negative", "category": "health"},

            # Achievement category
            {"text": "Achieved a goal", "mood_type": "positive", "category": "achievement"},
            {"text": "Learned something new", "mood_type": "positive", "category": "achievement"},
            {"text": "Made progress on project", "mood_type": "positive", "category": "achievement"},

            # Generic/Other
            {"text": "Other reason", "mood_type": "neutral", "category": "other", "is_generic": True},
        ]

        # Create all reasons
        created_reasons = []
        for reason_data in reasons_data:
            reason, created = Reason.objects.get_or_create(
                text=reason_data["text"],
                defaults={
                    "mood_type": reason_data["mood_type"],
                    "category": reason_data["category"],
                    "is_generic": reason_data.get("is_generic", False)
                }
            )
            created_reasons.append(reason)
            if created:
                self.stdout.write(f"  Created reason: {reason.text}")

        # Create actions
        actions_data = [
            # Rest/Sleep actions
            {"text": "Take a 20-minute power nap", "category": "rest"},
            {"text": "Go to bed earlier", "category": "rest"},
            {"text": "Create a relaxing bedtime routine", "category": "rest"},
            {"text": "Use white noise or calming music", "category": "rest"},

            # Social actions
            {"text": "Call a friend or family member", "category": "social"},
            {"text": "Meet someone for coffee", "category": "social"},
            {"text": "Join a group activity", "category": "social"},
            {"text": "Send a message to someone you care about", "category": "social"},

            # Physical Activity
            {"text": "Go for a walk outside", "category": "activity"},
            {"text": "Do some stretching", "category": "activity"},
            {"text": "Exercise for 15 minutes", "category": "activity"},
            {"text": "Try yoga", "category": "activity"},

            # Mindfulness
            {"text": "Practice deep breathing", "category": "mindfulness"},
            {"text": "Try meditation for 5 minutes", "category": "mindfulness"},
            {"text": "Write in a journal", "category": "mindfulness"},
            {"text": "Practice gratitude", "category": "mindfulness"},

            # Creative
            {"text": "Listen to music", "category": "creative"},
            {"text": "Draw or paint", "category": "creative"},
            {"text": "Read a book", "category": "creative"},
            {"text": "Watch something funny", "category": "creative"},

            # Generic actions (for 'Other' reasons)
            {"text": "Take time for yourself", "category": "other", "is_generic": True},
            {"text": "Do something you enjoy", "category": "other", "is_generic": True},
            {"text": "Change your environment", "category": "other", "is_generic": True},
            {"text": "Talk to someone", "category": "other", "is_generic": True},
        ]

        for action_data in actions_data:
            action, created = Action.objects.get_or_create(
                text=action_data["text"],
                defaults={
                    "category": action_data["category"],
                    "is_generic": action_data.get("is_generic", False)
                }
            )
     
            if created:
                self.stdout.write(f"  Created action: {action.text}")
      
            # Connect actions to relevant reasons based on category
            if not action_data.get("is_generic", False):
                if action.category == "rest":
                    # Connect to sleep-related reasons
                    sleep_reasons = Reason.objects.filter(category="sleep")
                    action.reasons.add(*sleep_reasons)
                    self.stdout.write(f"    Connected to {sleep_reasons.count()} sleep reasons")
          
                elif action.category == "social":
                    # Connect to relationship reasons
                    relationship_reasons = Reason.objects.filter(category="relationships")
                    action.reasons.add(*relationship_reasons)
           
                elif action.category == "activity":
                    # Connect to health and energy reasons
                    health_reasons = Reason.objects.filter(
                        category__in=["health", "sleep"]
                    )
                    action.reasons.add(*health_reasons)
  
        # Summary
        self.stdout.write(self.style.SUCCESS(
            f'\nSuccessfully seeded:'
            f'\n  {Reason.objects.count()} reasons'
            f'\n  {Action.objects.count()} actions'
        ))
