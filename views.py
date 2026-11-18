from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SchoolRegistrationForm, SchoolActivityForm

from .models import (
    School,
    Sport,
    SchoolSport,
    Competition,
    SchoolCompetition,
    Career,
    TVETProgram,
    SchoolAccount,
    SchoolRegistrationRequest,
    SchoolActivity,
)


# ==========================================================
# HOME
# ==========================================================

def home(request):
    schools = School.objects.all().order_by("name")[:6]

    school_count = School.objects.count()

    district_count = (
        School.objects
        .exclude(district__isnull=True)
        .exclude(district="")
        .values("district")
        .distinct()
        .count()
    )

    competition_count = Competition.objects.count()
    sport_count = Sport.objects.count()

    return render(
        request,
        "index.html",
        {
            "schools": schools,
            "school_count": school_count,
            "district_count": district_count,
            "competition_count": competition_count,
            "sport_count": sport_count,
        },
    )


# ==========================================================
# EXPLORE SCHOOLS
# ==========================================================

def schools_page(request):
    schools = School.objects.all().order_by("name")

    search = request.GET.get("search", "").strip()
    district = request.GET.get("district", "").strip()
    school_type = request.GET.get("school_type", "").strip()
    ownership = request.GET.get("ownership", "").strip()

    if search:
        search_words = search.split()

        for word in search_words:
            schools = schools.filter(
                Q(name__icontains=word)
                | Q(district__icontains=word)
                | Q(province__icontains=word)
                | Q(description__icontains=word)
                | Q(school_type__icontains=word)
                | Q(ownership__icontains=word)
            )

    if district:
        schools = schools.filter(district__iexact=district)

    if school_type:
        schools = schools.filter(school_type__iexact=school_type)

    if ownership:
        schools = schools.filter(ownership__iexact=ownership)

    districts = (
        School.objects
        .exclude(district__isnull=True)
        .exclude(district="")
        .values_list("district", flat=True)
        .distinct()
        .order_by("district")
    )

    school_types = (
        School.objects
        .exclude(school_type__isnull=True)
        .exclude(school_type="")
        .values_list("school_type", flat=True)
        .distinct()
        .order_by("school_type")
    )

    ownerships = (
        School.objects
        .exclude(ownership__isnull=True)
        .exclude(ownership="")
        .values_list("ownership", flat=True)
        .distinct()
        .order_by("ownership")
    )

    return render(
        request,
        "schools.html",
        {
            "schools": schools,
            "search": search,
            "district": district,
            "school_type": school_type,
            "ownership": ownership,
            "districts": districts,
            "school_types": school_types,
            "ownerships": ownerships,
        },
    )


# ==========================================================
# SCHOOL DETAIL
# ==========================================================

def school_detail(request, school_id):
    school = get_object_or_404(School, id=school_id)

    school_sports = (
        SchoolSport.objects
        .filter(school=school)
        .select_related("sport")
    )

    school_competitions = (
        SchoolCompetition.objects
        .filter(school=school)
        .select_related("competition")
        .order_by("-year", "position")
    )

    activities = (
        SchoolActivity.objects
        .filter(
            school=school,
            is_published=True,
        )
        .order_by("-activity_date", "-created_at")
    )

    return render(
        request,
        "school_detail.html",
        {
            "school": school,
            "school_sports": school_sports,
            "school_competitions": school_competitions,
            "activities": activities,
        },
    )


# ==========================================================
# COMPARE SCHOOLS
# ==========================================================

def compare_schools(request):
    selected_ids = request.GET.getlist("compare")

    selected_schools = School.objects.filter(
        id__in=selected_ids
    ).order_by("name")

    all_schools = School.objects.all().order_by("name")

    comparison_error = None

    if len(selected_ids) > 4:
        comparison_error = "You can compare up to 4 schools at a time."

        selected_ids = selected_ids[:4]

        selected_schools = School.objects.filter(
            id__in=selected_ids
        ).order_by("name")

    if not selected_ids:
        comparison_error = None

    return render(
        request,
        "compare.html",
        {
            "schools": all_schools,
            "selected_schools": selected_schools,
            "selected_ids": selected_ids,
            "comparison_error": comparison_error,
        },
    )


# ==========================================================
# TOP SCHOOLS
# ==========================================================

def top_schools(request):
    schools = School.objects.all().order_by("name")

    return render(
        request,
        "top_schools.html",
        {
            "schools": schools,
        },
    )


# ==========================================================
# SPORTS
# ==========================================================

def sports(request):
    sports_list = (
        Sport.objects
        .all()
        .order_by("name")
    )

    school_sports = (
        SchoolSport.objects
        .select_related("school", "sport")
        .order_by("sport__name", "school__name")
    )

    selected_sport = request.GET.get("sport", "").strip()

    if selected_sport:
        school_sports = school_sports.filter(
            sport_id=selected_sport
        )

    return render(
        request,
        "sports.html",
        {
            "sports": sports_list,
            "school_sports": school_sports,
            "selected_sport": selected_sport,
        },
    )


# ==========================================================
# COMPETITIONS
# ==========================================================

def competitions(request):
    competitions_list = (
        Competition.objects
        .annotate(
            school_entry_count=Count(
                "participating_schools"
            )
        )
        .all()
        .order_by("name")
    )

    school_competitions = (
        SchoolCompetition.objects
        .select_related(
            "school",
            "competition",
        )
        .all()
        .order_by(
            "competition__name",
            "-year",
            "position",
        )
    )

    selected_competition = request.GET.get(
        "competition",
        "",
    ).strip()

    if selected_competition:
        school_competitions = school_competitions.filter(
            competition_id=selected_competition
        )

    return render(
        request,
        "competitions.html",
        {
            "competitions": competitions_list,
            "school_competitions": school_competitions,
            "selected_competition": selected_competition,
        },
    )


# ==========================================================
# COMPETITION DETAIL
# ==========================================================

def competition_detail(request, competition_id):
    competition = get_object_or_404(
        Competition,
        id=competition_id,
        publication_status="published",
    )

    participating_schools = (
        SchoolCompetition.objects
        .filter(competition=competition)
        .select_related("school")
        .order_by("-year", "position")
    )

    gallery = (
        competition.gallery
        .all()
        .order_by("-created_at")
    )

    documents = (
        competition.documents
        .all()
        .order_by("-created_at")
    )

    return render(
        request,
        "competition_detail.html",
        {
            "competition": competition,
            "participating_schools": participating_schools,
            "gallery": gallery,
            "documents": documents,
        },
    )


# ==========================================================
# CAREERS & TVET
# ==========================================================

def careers(request):
    search = request.GET.get(
        "search",
        "",
    ).strip()

    careers_list = (
        Career.objects
        .all()
        .order_by("name")
    )

    tvet_programs = (
        TVETProgram.objects
        .all()
        .order_by("name")
    )

    if search:
        search_words = search.split()

        for word in search_words:
            careers_list = careers_list.filter(
                Q(name__icontains=word)
                | Q(category__icontains=word)
                | Q(description__icontains=word)
                | Q(subjects__icontains=word)
                | Q(skills__icontains=word)
            )

        for word in search_words:
            tvet_programs = tvet_programs.filter(
                Q(name__icontains=word)
                | Q(institution__icontains=word)
                | Q(category__icontains=word)
                | Q(description__icontains=word)
                | Q(entry_requirements__icontains=word)
                | Q(duration__icontains=word)
            )

    career_categories = (
        Career.objects
        .exclude(category="")
        .values_list(
            "category",
            flat=True,
        )
        .distinct()
        .order_by("category")
    )

    tvet_categories = (
        TVETProgram.objects
        .exclude(category="")
        .values_list(
            "category",
            flat=True,
        )
        .distinct()
        .order_by("category")
    )

    return render(
        request,
        "careers.html",
        {
            "careers": careers_list,
            "tvet_programs": tvet_programs,
            "career_categories": career_categories,
            "tvet_categories": tvet_categories,
            "search": search,
        },
    )


# ==========================================================
# SCHOOL REGISTRATION
# ==========================================================

def register_school(request):
    if request.method == "POST":
        form = SchoolRegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                (
                    "Your school registration request "
                    "has been submitted successfully. "
                    "Our team will review it."
                ),
            )

            return redirect(
                "registration_success"
            )

    else:
        form = SchoolRegistrationForm()

    return render(
        request,
        "register_school.html",
        {
            "form": form,
        },
    )


# ==========================================================
# REGISTRATION SUCCESS
# ==========================================================

def registration_success(request):
    return render(
        request,
        "registration_success.html",
    )


# ==========================================================
# SCHOOL LOGIN
# ==========================================================

def school_login(request):
    if request.user.is_authenticated:
        try:
            request.user.school_account
            return redirect("school_dashboard")
        except SchoolAccount.DoesNotExist:
            pass

    if request.method == "POST":
        email = request.POST.get(
            "email",
            "",
        ).strip()

        password = request.POST.get(
            "password",
            "",
        )

        try:
            school_account = (
                SchoolAccount.objects
                .select_related(
                    "school",
                    "user",
                )
                .get(
                    email__iexact=email
                )
            )
        except SchoolAccount.DoesNotExist:
            messages.error(
                request,
                "No school account was found with that email.",
            )

            return render(
                request,
                "school_login.html",
            )

        if not school_account.user:
            messages.error(
                request,
                (
                    "This school account has not "
                    "been activated yet. Please wait "
                    "for administrator approval."
                ),
            )

            return render(
                request,
                "school_login.html",
            )

        user = authenticate(
            request,
            username=school_account.user.username,
            password=password,
        )

        if user is not None:
            if school_account.status in [
                "rejected",
                "suspended",
            ]:
                messages.error(
                    request,
                    "This school account is not currently active.",
                )

                return render(
                    request,
                    "school_login.html",
                )

            login(
                request,
                user,
            )

            return redirect(
                "school_dashboard"
            )

        messages.error(
            request,
            "Invalid email or password.",
        )

    return render(
        request,
        "school_login.html",
    )


# ==========================================================
# SCHOOL DASHBOARD
# ==========================================================

@login_required(login_url="school_login")
def school_dashboard(request):
    try:
        school_account = (
            SchoolAccount.objects
            .select_related(
                "school",
                "user",
            )
            .get(
                user=request.user
            )
        )

    except SchoolAccount.DoesNotExist:
        messages.error(
            request,
            "Your account is not connected to a school.",
        )

        logout(request)

        return redirect(
            "school_login"
        )

    school = school_account.school

    activities = (
        SchoolActivity.objects
        .filter(school=school)
        .order_by(
            "-activity_date",
            "-created_at",
        )
    )

    return render(
        request,
        "school_dashboard.html",
        {
            "school_account": school_account,
            "school": school,
            "activities": activities,
        },
    )


# ==========================================================
# CREATE SCHOOL ACTIVITY
# ==========================================================

@login_required(login_url="school_login")
def create_school_activity(request):
    try:
        school_account = (
            SchoolAccount.objects
            .select_related("school")
            .get(
                user=request.user
            )
        )

    except SchoolAccount.DoesNotExist:
        messages.error(
            request,
            "Your account is not connected to a school.",
        )

        return redirect(
            "school_login"
        )

    if request.method == "POST":
        form = SchoolActivityForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            activity = form.save(
                commit=False
            )

            activity.school = school_account.school

            # Activities created by schools remain
            # unpublished until approved in admin.
            activity.is_published = False

            activity.save()

            messages.success(
                request,
                (
                    "Your activity was submitted "
                    "successfully and is waiting for publication."
                ),
            )

            return redirect(
                "school_dashboard"
            )

    else:
        form = SchoolActivityForm()

    return render(
        request,
        "create_school_activity.html",
        {
            "form": form,
            "school": school_account.school,
        },
    )


# ==========================================================
# SCHOOL LOGOUT
# ==========================================================

@login_required(login_url="school_login")
def school_logout(request):
    logout(request)

    messages.success(
        request,
        "You have been logged out successfully.",
    )

    return redirect(
        "school_login"
    )


# ==========================================================
# EVENTS & NEWS
# ==========================================================

def events_news(request):
    events = (
        SchoolActivity.objects
        .filter(
            is_published=True
        )
        .select_related("school")
        .order_by(
            "-activity_date",
            "-created_at",
        )
    )

    return render(
        request,
        "events_news.html",
        {
            "events": events,
        },
    )


# ==========================================================
# EVENT DETAIL
# ==========================================================

def event_detail(request, event_id):
    event = get_object_or_404(
        SchoolActivity.objects.select_related(
            "school"
        ),
        id=event_id,
        is_published=True,
    )

    return render(
        request,
        "event_detail.html",
        {
            "event": event,
        },
    )
# ==========================================================
# OPPORTUNITIES
# ==========================================================

def opportunities(request):

    search = request.GET.get("search", "").strip()
    category = request.GET.get("category", "").strip()

    opportunities_list = (
        Opportunity.objects
        .filter(is_published=True)
        .order_by(
            "-is_featured",
            "deadline",
            "-created_at",
        )
    )

    if search:
        opportunities_list = opportunities_list.filter(
            Q(title__icontains=search)
            | Q(organization__icontains=search)
            | Q(description__icontains=search)
            | Q(eligibility__icontains=search)
        )

    if category:
        opportunities_list = opportunities_list.filter(
            category=category
        )

    opportunity_categories = (
        Opportunity.objects
        .filter(is_published=True)
        .exclude(category="")
        .values_list("category", flat=True)
        .distinct()
        .order_by("category")
    )

    return render(
        request,
        "opportunities.html",
        {
            "opportunities": opportunities_list,
            "opportunity_categories": opportunity_categories,
            "search": search,
            "selected_category": category,
        },
    )


def opportunity_detail(request, opportunity_id):

    opportunity = get_object_or_404(
        Opportunity,
        id=opportunity_id,
        is_published=True,
    )

    return render(
        request,
        "opportunity_detail.html",
        {
            "opportunity": opportunity,
        },
    )