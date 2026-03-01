## Setup Instructions

1. Clone the repository
2. Create virtual environment
3. Install dependencies
4. **Run migrations:** `python manage.py migrate`
5. **Run seeds_data:** `python manage.py seed_data`
6. **Run collectstatic** `python manage.py collectstatic`
7. Start server: `python manage.py runserver`

## When Pulling Updates related to database

After any `git pull`, always run:
python manage.py migrate














# team1-Meta_Mood
[View the Live Project here]()

# Table of Content
- [User Expeience](#user-experience)
    - [Project Goals](#project-goals)
    - [User Stories](#user-stories)
    - [Design Choices](#design-choices)
    - [Wireframes](#wireframes)
- [App Logic](#app-logic)    
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Code](#code)
- [Testing](#testing)
    - [Bugs](#bugs-known-issues--solutions)
    - [Unresolved Bugs](#unresolved-bugs)
    - [Tesing User Stories](#testing-user-stories)
    - [Manual Testing](#manual-testing)
    - [Automated Testing](#automated-testing)
    - [Accessibility](#accessibility)
- [Deployment](#deployment)
- [Maintenance & Updates](#maintenance--updates)
- [Credits](#credits)

## User Experience

### Project Goals

People often experience changes in mood without clearly understanding what causes them. Everyday factors such as sleep, health, work, weather, or social interactions can have a strong impact on how we feel, but these patterns are easy to overlook. This app helps users quickly record their mood, select possible reasons, and choose simple actions that might improve their wellbeing.


By tracking moods, reasons, and actions over time, users can start to recognise patterns and discover what actually helps them feel better. The app is designed to be fast and simple to use, making it easy to build a habit of regular mood check-ins without overthinking the process.

### User Stories

**EPIC 1: Mood Check-in (Core Function)**

1.1 Recording Current State
- As a user I want to quickly log my current mood on a 5-point scale with matching emojis so that I can establish a baseline without overthinking it

- As a user who struggles to articulate feelings I want visual cues (colors and emojis) for each mood level so that I can select my mood intuitively

1.2 Identifying Drivers
- As a user reflecting on my day I want to select multiple tags that explain why I feel this way so that I can identify patterns in what affects my mood

- As a user with a unique situation I want to add a custom free-text note so that I can capture context that predefined tags miss

- As a forgetful user I want the driver tags to be relevant and reasonably comprehensive so that I don't miss important factors

**EPIC 2: Action Planning (Intervention)**

2.1 Receiving Suggestions
- As a user who wants to feel better I want the app to suggest actions based on my selected drivers and mood so that I don't have to figure out solutions when I'm already struggling

- As a user with specific preferences I want to select from suggested actions or create my own so that the action plan feels personalized and doable

- As a skeptical user I want to understand why certain actions are being suggested so that I trust the recommendations and am more likely to follow through

2.2 Commitment & Reminders
- As a busy user I want to confirm an action and set a follow-up reminder so that I can go live my life and remember to report back

- As a user who gets sidetracked I want a push notification after my chosen time interval so that I actually complete the feedback loop

**EPIC 3: Follow-up & Outcome Tracking**
3.1 Post-Action Check-in 
- As a user who tried an intervention I want to record my mood again after the action so that I can see if it actually helped

- As a user evaluating the action I want to rate how helpful the action was on a 1-5 scale so that I can track effectiveness over time

- As a user with additional thoughts I want to add a follow-up note so that I can capture nuances like "it helped but only temporarily"

3.2 Incomplete Cycles
- As a user who misses a follow-up I want the app to gently remind me once more (not spam me) so that I can still complete the loop without feeling pressured

- As a user who never completed a cycle I want incomplete entries to remain in my history with partial data so that I still have record of the initial mood even without outcome

The project's Kanban Board can be viewd [here](https://github.com/orgs/Coolafdood/projects/8/views/2)

### Design Choices

#### Fonts

#### Icons

#### Images

### Wireframes

## App Logic

### User Flow

#### Overview
A 3-step mood tracking application that helps users log their emotions, identify reasons, and track effective actions.

#### Step 1: Mood Selection
- User selects current mood on a 5-point scale:
      - 1 = Very bad
      - 2 = Bad
      - 3 = Neutral
      - 4 = Good
      - 5 = Excellent

#### Step 2: Reason Selection
- Based on mood, user sees relevant reasons (10-12 options)
- Reasons are organised by categories (Sleep, Weather, Work, Relationship, Health, Achievement)
- "Other" option available for custom reasons
- Selection saved in session

#### Step 3: Action Selection
- User received mood-appriopriate action suggestion:
    - Very bad mood(1) = "What might help you feel a little better?" (rest, mindfulness activities)
    - Bad mood(2) = "What could improve your mood?" (rest, mindfulness activities)
    - Neutral mood(3) = "What would you like to do today?" (balanced options)
    - Good mood(4) = "How would you like to enjoy this moment?" (enhancement activities)
    - Excellent mood(5) = "What would make this excellent day even better?" (enhancement activities)
 
#### Dashboard and Feedback
- view mood history and statistics
- Category-based insights with visual cards
- Feedback loop: After 1 hour, user is ased if the action helped (the time was shortened to 10s for testing)
- Track action effectiveness over time
- Selete entries if needed

#### Data Structure
- **Reasons:** Linked to mood types (negative/neutral/positive) and categories
- **Actions:** Connected to specific reasons with mood-appropriate suggestions
- **MoodEntries:** Complete log with mood, reason, action, and feedback

The app helps users understand their emotional patterns and discover what actually improves their mood!

`User selects mood (1-5) 
    → determines mood_type (negative/neutral/positive)
        → shows reasons with that mood_type
            → User selects specific reason
                → Shows ONLY actions linked to THAT reason`

## Features

## Technologies Used

## Code

## Testing

### Bugs, Known Issues & Solutions

#### Mood Label Mismatch
**Problem:** Step 3 showed "What might help you feel better?" even for excellent moods, which felt inappropriate.

**Solution:** Added dynamic labels based on mood value (1-5) with customized messages for each mood level.

#### Overwhelming Number of Options
**Problem:** Users faced 20+ reasons/actions to choose from, causing decision fatigue.

**Solution:** Implemented smart filtering that shows max 12 options (2 per category) with random selection for variety.

#### Feedback Form Not Appearing
**Problem:** Users never saw the follow-up question about whether actions helped.

**Solution:** Fixed timing logic in dashboard view and ensured session data persists correctly between steps.

#### Form Parameters Errors
**Problem:** `BaseForm.__init__() got an unexpected keyword argument` errors when passing custom querysets.

**Solution:** Properly popped all custom parameters before calling `super().__init__()` in form classes.

### Unresolved Bugs

### Testing User Stories

### Manual Testing

### Automated Testing

### Accessibility

## Deployment

## Maintenance & Updates

## Credits

### Content

### Media
























A human-centred dashboard that visualises emotional wellbeing trends using interactive frontend storytelling.

Problem Statement

What human issue are you solving?

Target Users

Be specific:

Students?

NHS workers?

Small businesses?

Young adults?

Local community?

Core Features

Frontend interaction

Data insight

Emotional UX

Optional backend support

Tech Stack

Frontend:

React / JS / HTML/CSS

Data:

Pandas

Matplotlib / Plotly

ML (if applicable)

Backend (optional):

Flask / Django / FastAPI

Ethics & Data Responsibility

This is important in this hackathon.
Add:

Data source

Privacy considerations

Bias mitigation

Accessibility

Project Structure

Show folder layout clearly.
