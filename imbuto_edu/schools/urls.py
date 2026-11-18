from django.urls import path
from . import views


urlpatterns = [
    # Home
    path(
        "",
        views.home,
        name="home",
    ),

    # Schools
    path(
        "schools/",
        views.schools_page,
        name="schools_page",
    ),

    path(
        "school/<int:school_id>/",
        views.school_detail,
        name="school_detail",
    ),

    # School comparison
    path(
        "compare/",
        views.compare_schools,
        name="compare_schools",
    ),

    # Rankings
    path(
        "top-schools/",
        views.top_schools,
        name="top_schools",
    ),

    # Sports
    path(
        "sports/",
        views.sports,
        name="sports",
    ),

    # Competitions
    path(
        "competitions/",
        views.competitions,
        name="competitions",
    ),
    path(
    'competitions/<int:competition_id>/',
    views.competition_detail,
    name='competition_detail',
    ),

    # Careers / TVET
    path(
        "careers/",
        views.careers,
        name="careers",
    ),

    # School registration
    path(
        "register-school/",
        views.register_school,
        name="register_school",
    ),

    path(
        "registration-success/",
        views.registration_success,
        name="registration_success",
    ),

    # School portal
    path(
        "school-login/",
        views.school_login,
        name="school_login",
    ),

    path(
        "school-dashboard/",
        views.school_dashboard,
        name="school_dashboard",
    ),

    path(
        "school-logout/",
        views.school_logout,
        name="school_logout",
    ),

    # Events & News
    path(
        "events-news/",
        views.events_news,
        name="events_news",
    ),

    path(
        "events-news/<int:event_id>/",
        views.event_detail,
        name="event_detail",
    ),

    # School dashboard activities
    path(
        "school-dashboard/create-activity/",
        views.create_school_activity,
        name="create_school_activity",
    ),
    path(
    "opportunities/",
    views.opportunities,
    name="opportunities",
),

path(
    "opportunities/<int:opportunity_id>/",
    views.opportunity_detail,
    name="opportunity_detail",
),
]