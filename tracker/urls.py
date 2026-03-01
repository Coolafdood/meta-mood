from django.urls import path
from . import views

app_name = "tracker"

urlpatterns = [
    path("", views.index, name="index"),
    path("step1/", views.step1_mood, name="step1_mood"),
    path("step2/", views.step2_reason, name="step2_reason"),
    path("step3/", views.step3_action, name="step3_action"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("feedback/<int:entry_id>/", views.submit_feedback, name="submit_feedback"),
    path("delete/<int:entry_id>/", views.delete_entry, name="delete_entry"),
]
