# team1-Meta_Mood
**[View the Live Project here](https://metamood-63b673a5590d.herokuapp.com/)**

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
    - [Tesing User Stories & Manual Testing](#testing-user-stories--manual-testing)
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

The project's Kanban Board can be viewd **[here](https://github.com/orgs/Coolafdood/projects/8/views/2)**

### Design Choices

### Wireframes

| Page | Desktop | Mobile |
|------|---------|--------|
| Home | <a href="https://github.com/Coolafdood/meta-mood/blob/main/docs/home.png"><img src="https://github.com/Coolafdood/meta-mood/blob/main/docs/home.png" width="200"></a> | — |
| About | <a href="https://github.com/Coolafdood/meta-mood/blob/main/docs/about-page-Desktop.png"><img src="https://github.com/Coolafdood/meta-mood/blob/main/docs/about-page-Desktop.png" width="200"></a> | — |
| Dashboard | <a href="https://github.com/Coolafdood/meta-mood/blob/main/docs/dashboard-Desktop.png"><img src="https://github.com/Coolafdood/meta-mood/blob/main/docs/dashboard-Desktop.png" width="200"></a> | <a href="https://github.com/Coolafdood/meta-mood/blob/main/docs/dashboard-Mobile.png"><img src="https://github.com/Coolafdood/meta-mood/blob/main/docs/dashboard-Mobile.png" width="200"></a> |
| Check-in | — | <a href="https://github.com/Coolafdood/meta-mood/blob/main/docs/checkin-page-Mobile.png"><img src="https://github.com/Coolafdood/meta-mood/blob/main/docs/checkin-page-Mobile.png" width="200"></a> |
| Insights | <a href="https://github.com/Coolafdood/meta-mood/blob/main/docs/insight-analytics-Desktop.png"><img src="https://github.com/Coolafdood/meta-mood/blob/main/docs/insight-analytics-Desktop.png" width="200"></a> | <a href="https://github.com/Coolafdood/meta-mood/blob/main/docs/insight-analytics-Mobile.png"><img src="https://github.com/Coolafdood/meta-mood/blob/main/docs/insight-analytics-Mobile.png" width="200"></a> |
| Login | <a href="https://github.com/Coolafdood/meta-mood/blob/main/docs/login.png"><img src="https://github.com/Coolafdood/meta-mood/blob/main/docs/login.png" width="200"></a> | <a href="https://github.com/Coolafdood/meta-mood/blob/main/docs/loginpage-mobile.png"><img src="https://github.com/Coolafdood/meta-mood/blob/main/docs/loginpage-mobile.png" width="200"></a> |
| Sign Up | <a href="https://github.com/Coolafdood/meta-mood/blob/main/docs/Sign-Up-Page-Desktop.png"><img src="https://github.com/Coolafdood/meta-mood/blob/main/docs/Sign-Up-Page-Desktop.png" width="200"></a> | <a href="https://github.com/Coolafdood/meta-mood/blob/main/docs/sign-up-Mobile.png"><img src="https://github.com/Coolafdood/meta-mood/blob/main/docs/sign-up-Mobile.png" width="200"></a> |
| Password Reset | <a href="https://github.com/Coolafdood/meta-mood/blob/main/docs/Password-reset-request-Desktop.png"><img src="https://github.com/Coolafdood/meta-mood/blob/main/docs/Password-reset-request-Desktop.png" width="200"></a> | — |

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

**1. Languages:**
- Python - the core programming language used to build the application.
- HTML5 - the standard markup language for structuring content on the web.
- CSS 
- JavaScript - added interactivity and client-side behaviour.

**2. Frameworks & Libraries:**
- Django - the main web framework used to manage models, views, templates, authentication, and admin functionality.
- Django Allauth - user authentication, signup, and login with social account support.

**3. Database & Deployment:**
- PostgreSQL - relational database used in production.
- psycopg2 - PostgreSQL database adapter for Python/Django.
- Gunicorn - Python WSGI HTTP server for running Django apps in production.
- Whitenoise – serves static files efficiently in Django without extra servers.
- dj-database-url – allows database configuration via environment variables (useful for deployment).
- [Heroku](https://www.heroku.com/) - platform-as-a-service (PaaS) used to deploy, manage, and scale the live application.

**Version Control:**
- Git – version control system to track and manage code changes.
- GitHub – remote repository hosting, project board, and collaboration tool.

## Resources & Tools

- [mermaidchart](https://www.mermaidchart.com/) to draw Entity-Relationship Diagram.
- [Open AI](https://openai.com/chatgpt/overview/) to create / review the content for spelling, grammar and consistency; to ask for suggestions on how to solve certain problems.
- [deepseek](https://www.deepseek.com/en) to solve and explain certain problems.

## Code

## Testing

### Bugs, Known Issues & Solutions

1. Mood Label Mismatch
**Problem:** Step 3 showed "What might help you feel better?" even for excellent moods, which felt inappropriate.

**Solution:** Added dynamic labels based on mood value (1-5) with customized messages for each mood level.

2. Overwhelming Number of Options
**Problem:** Users faced 20+ reasons/actions to choose from, causing decision fatigue.

**Solution:** Implemented smart filtering that shows max 12 options (2 per category) with random selection for variety.

3. Feedback Form Not Appearing
**Problem:** Users never saw the follow-up question about whether actions helped.

**Solution:** Fixed timing logic in dashboard view and ensured session data persists correctly between steps.

4. Form Parameters Errors
**Problem:** `BaseForm.__init__() got an unexpected keyword argument` errors when passing custom querysets.

**Solution:** Properly popped all custom parameters before calling `super().__init__()` in form classes.

5. Feedback Form Not Showing for Old Entries
**Problem:** Feedback form only appeared for the most recent entry. Making a new entry would hide previous feedback opportunities.

**Fix:** Changed from session-based to database query that checks ALL entries needing feedback (action exists, no feedback yet, time passed).

6. Custom Actions Not Trackable
**Problem:** Custom actions ("Something else") were only saved in notes, not linked to an Action object. They didn't appear in tables and couldn't receive feedback.

**Fix:** Created generic "Custom action" object and linked it to entries while preserving original text in notes.

7. Custom Reason/Action Text Mix-up
**Problem:** When users entered both custom reason AND custom action, both texts were saved in the same notes field, causing them to appear in both columns.

**Fix:** Added model properties (display_reason, display_action) to properly extract and separate custom texts.

### Unresolved Bugs

### Testing User Stories & Manual Testing

| ID  | Feature          | Test Description      | Steps                             | Expected Result  | Result |
| --- | ---------------- | --------------------- | --------------------------------- | ---------------- | ------ |
| T1  | Mood Selection   | User selects a mood   | Select mood → Click Next          | Next page loads  |  Pass  |
| T2  | Mood Selection   | Mood is required      | Click Next without selecting mood | Nothing happens  |  Pass  |
| T3  | Reason Selection | Reasons are displayed | Go to Step 2                      | Reasons visible  |  Pass  | 
| T5  | Reason Selection | Other reason          | Select "Other"                    | Saved correctly  |  Pass  |
| T6  | Action Selection | Actions displayed     | Go to Step 3                      | Actions visible  |  Pass  |
| T7  | Action Selection | Select action         | Select action → Save              | Entry saved      |  Pass  |
| T8  | Dashboard        | Entries visible       | Open dashboard                    | Entries shown    |  Pass  |
| T9  | Dashboard        | New entry visible     | Add entry → Dashboard             | Entry visible    |    Pass|
| T10 | Feedback         | Feedback question     | Wait → Return                     | Question visible |  Pass  |
| T11 | Feedback         | Yes feedback          | Click Yes                         | Saved            |  Pass  |
| T12 | Feedback         | No feedback           | Click No                          | Saved            |  Pass  |
| T13 | Navigation       | Step navigation       | Complete steps                    | Works correctly  |  Pass  |
| T14 | Colours          | Mood colours          | View moods                        | Colours correct  |  Pass  |
| T15 | Emojis           | Mood emojis           | View moods                        | Emojis visible   |  Pass  |
| T16 | Mobile           | Responsive layout     | Open on phone                     | Layout works     |   Pass |
| T17 | 404 Page         | Invalid URL           | Go to wrong URL                   | 404 page shown   |   Pass |
| T18 | 500 Page         | Server error          | Trigger error                     | 500 page shown   |   Pass |
| T19 | Empty Dashboard  | No entries            | Open dashboard                    | Message shown    |  Pass  |
| T20 | Delete Entry     | Delete entry          | Click delete                      | Entry removed    |  Pass  |


### Automated Testing

**Test Results**

The project currently includes approximately 35 automated tests covering:

- Models
- Forms
- Views
- Statistics
- Feedback

All tests are passing successfully:

1. test_models.py - Database Models **[click here](https://github.com/Coolafdood/meta-mood/blob/main/tracker/tests/test_models.py)**

| Test                              | What it Checks                                                |
| --------------------------------- | ------------------------------------------------------------- |
| `test_reason_creation`            | Reasons are created with correct fields (mood_type, category) |
| `test_action_creation`            | Actions are created with correct fields                       |
| `test_action_reason_relationship` | Many-to-many link between actions and reasons works           |
| `test_mood_entry_creation`        | Mood entries save all fields correctly                        |
| `test_mood_entry_str_method`      | String representation of mood entry works                     |
| `test_helper_properties`          | `day_of_week`, `month`, `hour` properties work                |

2. test_forms.py - Form Validation **[click here](https://github.com/Coolafdood/meta-mood/blob/main/tracker/tests/test_forms.py)**

| Test                                   | What it Checks                         |
| -------------------------------------- | -------------------------------------- |
| `test_step1_form_valid`                | Step 1 accepts valid mood (1–5)        |
| `test_step1_form_invalid`              | Step 1 rejects invalid mood (e.g. 6)   |
| `test_step2_form_positive_mood`        | Shows only positive reasons for mood 5 |
| `test_step2_form_negative_mood`        | Shows only negative reasons for mood 1 |
| `test_step2_form_neutral_mood`         | Shows only neutral reasons for mood 3  |
| `test_step2_form_with_custom_queryset` | Form accepts custom reason list        |
| `test_step3_form_for_positive_reason`  | Shows correct label for positive mood  |
| `test_step3_form_for_negative_reason`  | Shows correct label for negative mood  |
| `test_step3_form_custom_reason`        | Handles custom reasons correctly       |
| `test_feedback_form`                   | Feedback form has yes/no options       |

3. test_views.py – Page Loads & User Flow **[click here](https://github.com/Coolafdood/meta-mood/blob/main/tracker/tests/test_views.py)**

| Test                                  | What it Checks                            |
| ------------------------------------- | ----------------------------------------- |
| `test_index_view`                     | Landing page loads                        |
| `test_index_view_anonymous`           | Landing page works for anonymous users    |
| `test_step1_view_get`                 | Step 1 page loads with form               |
| `test_step1_view_post`                | Step 1 form submits and sets session      |
| `test_step2_view_redirect_if_no_mood` | Redirects to Step 1 if no mood in session |
| `test_step2_view_with_mood`           | Step 2 loads when mood exists in session  |
| `test_step2_view_post_reason`         | Step 2 saves reason to session            |
| `test_step2_view_post_custom`         | Step 2 handles "Other" reason             |
| `test_step3_view_with_valid_data`     | Complete flow creates MoodEntry           |

4. test_statistics.py – Dashboard Calculations **[click here](https://github.com/Coolafdood/meta-mood/blob/main/tracker/tests/test_statistics.py)**

| Test                                   | What it Checks                                    |
| -------------------------------------- | ------------------------------------------------- |
| `test_total_entries_count`             | Counts total entries correctly                    |
| `test_average_mood_calculation`        | Calculates average mood correctly                 |
| `test_positive_percentage_calculation` | Calculates percentage of positive moods correctly |
| `test_category_filtering_threshold`    | Only shows categories with enough entries         |
| `test_top_reasons_ordering`            | Orders reasons by frequency                       |
| `test_recent_entries_ordering`         | Shows newest entries first                        |

5. test_feedback.py – Action Feedback **[click here](https://github.com/Coolafdood/meta-mood/blob/main/tracker/tests/test_feedback.py)**

| Test                                  | What it Checks                            |
| ------------------------------------- | ----------------------------------------- |
| `test_feedback_not_shown_immediately` | Feedback form does not appear immediately |
| `test_feedback_submission_yes`        | "Yes" feedback saves correctly            |
| `test_feedback_submission_no`         | "No" feedback saves correctly             |
| `test_feedback_only_once`             | Feedback cannot be submitted twice        |
| `test_feedback_wrong_user`            | Users cannot submit feedback for others   |
| `test_delete_entry`                   | Users can delete their own entries        |
| `test_delete_entry_wrong_user`        | Users cannot delete others' entries       |

**Running tests**

To run all automated tests, use `python manage.py test tracker`

### Accessibility

Accessibility was considered throughout the design and implementation of the application to ensure it is usable by a wide range of users.

- **Semantic HTML** is used to provide meaningful structure for screen readers and assistive technologies.
- **Responsive design** implemented with Tailwind CSS ensures the interface works across different screen sizes and devices.
- **Sufficient colour contrast** is maintained between text, backgrounds, and interactive elements to improve readability.
- **Clear visual hierarchy** using consistent headings, spacing, and font sizes helps users easily navigate content.
- **Keyboard accessibility** is supported through standard HTML controls (links, buttons, forms) and visible focus states.
- **Alternative text** is provided for animal images, with meaningful alt attributes based on animal names.
- **Form inputs** include labels or accessible attributes (such as aria-label) to support screen reader users.
- **Motion and effects** are kept subtle to avoid unnecessary visual distraction.

## Deployment

The website was deployed to Heroku and can be found **[here](https://metamood-63b673a5590d.herokuapp.com/)**.

- Heroku is a cloud platform that lets developers create, deploy, monitor and manage apps.
- You will need a Heroku log-in to be able to deploy a website to Heroku.
- Once you have logged into Heroku:
- Click 'New' > 'Create new app'
- Choose a unique name, choose your region and press 'Create app'
- Click on 'Settings' and then 'Reveal Config Vars'
- Add a key of 'DATABASE_URL' - the value will be the URL you were emailed when creating your database.
- Add a key of 'SECRET_KEY' - the value will be any random secret key (google 'secret key generator' and use it to generate a random string of numbers, letters and characters)
- In your terminal, type the code you will need to install project requirements:
  - pip3 install gunicorn
  - pip install whitenoise
  - pip3 install -r requirements.txt
  - pip3 freeze --local > requirements.txt
- Create an 'env.py' file at the root directory which contains the following:
  - import os
  - os.environ["DATABASE_URL"]='CI database URL'
  - os.environ["SECRET_KEY"]=" Your secret key"
- Create a file at the root directory called Procfile. In this file enter: "web: gunicorn my_project.wsgi" (without the quotes)
- Create a file at the root directory called runtime.txt. In this file enter your Python version (`python -V`)
- In settings.py, set DEBUG to False.
- YOU SHOULD ALWAYS SET DEBUG TO FALSE BEFORE DEPLOYING FOR SECURITY
- Add ",'.herokuapp.com' " (without the double quotes) to the ALLOWED_HOSTS list in settings.py
- Add, commit and push your code.
- Go back to Heroku, click on the 'Deploy' tab.
- Connect your project to GitHub.
- Scroll to the bottom and click 'Deploy Branch' and your project will be deployed!

## Maintenance & Updates

### Planned Features

We had big dreams for this project! Here's what we'd love to add when we have more time:

**Interactive Analytics Dashboard**
- Mood Over Time Charts - Line graphs showing emotional patterns and trends
- Trigger Analysis - Pie charts visualising which categories affect your mood most
- Action Effectiveness - Bar charts showing which strategies actually help (based on feedback)
- Weekly/Monthly Comparisons - See how your mood changes over different time periods

**Coming Soon Ideas**
- Email/Daily Reminders - Gentle nudges to log your mood
- Export Data - Download your mood history as CSV/PDF
- Mood Predictions - Simple AI to predict mood based on patterns
- Social Features - Share anonymised insights with friends (opt-in)
- Mobile Responsiveness - Better experience on phones
