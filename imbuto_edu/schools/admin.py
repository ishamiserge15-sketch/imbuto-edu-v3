from django.contrib import admin, messages
from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone
from django.utils.crypto import get_random_string

from .models import (
    School,
    Sport,
    SchoolSport,
    Competition,
    CompetitionGallery,
    CompetitionDocument,
    SchoolCompetition,
    Career,
    TVETProgram,
    SchoolAccount,
    SchoolVerification,
    SchoolRegistrationRequest,
    SchoolActivity,
    Opportunity,
)


# ==========================================================
# SCHOOL REGISTRATION APPROVAL
# ==========================================================

@admin.action(description="Approve selected requests & create school accounts")
def approve_registration_requests(modeladmin, request, queryset):

    approved_count = 0
    skipped_count = 0

    for registration in queryset:

        if registration.status != "pending":
            skipped_count += 1
            continue

        try:
            with transaction.atomic():

                school = School.objects.create(
                    name=registration.school_name,
                    district=registration.district,
                    province=registration.province,
                    category=registration.school_type,
                    school_type="Mixed",
                    ownership=normalize_ownership(
                        registration.ownership
                    ),
                    email=registration.email,
                    phone=registration.phone,
                    website=registration.website,
                    description=registration.message,
                )

                base_username = (
                    registration.email
                    .split("@")[0]
                    .strip()
                    .lower()
                )

                username = base_username
                counter = 1

                while User.objects.filter(
                    username=username
                ).exists():

                    username = f"{base_username}{counter}"
                    counter += 1

                temporary_password = get_random_string(
                    length=14,
                    allowed_chars=(
                        "abcdefghijkmnopqrstuvwxyz"
                        "ABCDEFGHJKLMNPQRSTUVWXYZ"
                        "23456789"
                        "!@#$%"
                    )
                )

                user = User.objects.create_user(
                    username=username,
                    email=registration.email,
                    password=temporary_password,
                    first_name=registration.contact_person,
                )

                SchoolAccount.objects.create(
                    school=school,
                    user=user,
                    email=registration.email,
                    phone=registration.phone,
                    status="verified",
                )

                SchoolVerification.objects.create(
                    school=school,
                    status="approved",
                    reviewer_notes=registration.admin_notes,
                )

                registration.status = "approved"
                registration.save(
                    update_fields=["status"]
                )

                messages.success(
                    request,
                    (
                        f"APPROVED: {school.name} | "
                        f"Email: {registration.email} | "
                        f"Username: {username} | "
                        f"Temporary password: {temporary_password}"
                    )
                )

                approved_count += 1

        except Exception as error:

            messages.error(
                request,
                (
                    f"Could not approve "
                    f"{registration.school_name}: {error}"
                )
            )

    if skipped_count:
        messages.warning(
            request,
            (
                f"{skipped_count} request(s) were skipped "
                f"because they were already processed."
            )
        )

    if approved_count:
        messages.info(
            request,
            (
                f"{approved_count} school registration "
                f"request(s) approved successfully."
            )
        )


def normalize_ownership(value):

    value = value.strip().lower()

    if value in ["government", "public"]:
        return "Government"

    if value in ["private"]:
        return "Private"

    if value in [
        "faith-based",
        "faith based",
        "faithbased",
    ]:
        return "Faith-Based"

    return "Private"


# ==========================================================
# REGISTRATION REQUEST ADMIN
# ==========================================================

@admin.register(SchoolRegistrationRequest)
class SchoolRegistrationRequestAdmin(admin.ModelAdmin):

    list_display = (
        "school_name",
        "district",
        "province",
        "contact_person",
        "email",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "province",
        "district",
        "created_at",
    )

    search_fields = (
        "school_name",
        "contact_person",
        "email",
        "phone",
        "district",
    )

    readonly_fields = (
        "created_at",
        "reviewed_at",
    )

    actions = [
        approve_registration_requests,
    ]

    ordering = (
        "-created_at",
    )


# ==========================================================
# SCHOOL
# ==========================================================

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "district",
        "province",
        "category",
        "school_type",
        "ownership",
        "email",
    )

    list_filter = (
        "province",
        "district",
        "category",
        "school_type",
        "ownership",
    )

    search_fields = (
        "name",
        "district",
        "province",
        "email",
    )


# ==========================================================
# SCHOOL ACCOUNT
# ==========================================================

@admin.register(SchoolAccount)
class SchoolAccountAdmin(admin.ModelAdmin):

    list_display = (
        "school",
        "email",
        "status",
        "user",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "school__name",
        "email",
        "phone",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


# ==========================================================
# SCHOOL VERIFICATION
# ==========================================================

@admin.register(SchoolVerification)
class SchoolVerificationAdmin(admin.ModelAdmin):

    list_display = (
        "school",
        "status",
        "submitted_at",
        "reviewed_at",
    )

    list_filter = (
        "status",
        "submitted_at",
    )

    search_fields = (
        "school__name",
    )

    readonly_fields = (
        "submitted_at",
    )


# ==========================================================
# SPORTS
# ==========================================================

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):

    list_display = (
        "name",
    )

    search_fields = (
        "name",
    )


@admin.register(SchoolSport)
class SchoolSportAdmin(admin.ModelAdmin):

    list_display = (
        "school",
        "sport",
        "achievement",
    )

    list_filter = (
        "sport",
    )

    search_fields = (
        "school__name",
        "sport__name",
    )


# ==========================================================
# COMPETITION GALLERY INLINE
# ==========================================================

class CompetitionGalleryInline(admin.TabularInline):

    model = CompetitionGallery

    extra = 1

    fields = (
        "image",
        "caption",
    )


# ==========================================================
# COMPETITION DOCUMENT INLINE
# ==========================================================

class CompetitionDocumentInline(admin.TabularInline):

    model = CompetitionDocument

    extra = 1

    fields = (
        "title",
        "document",
        "description",
    )


# ==========================================================
# SCHOOL COMPETITION / RESULTS INLINE
# ==========================================================

class SchoolCompetitionInline(admin.TabularInline):

    model = SchoolCompetition

    extra = 1

    fields = (
        "school",
        "year",
        "position",
        "achievement",
    )

    ordering = (
        "-year",
        "position",
    )


# ==========================================================
# COMPETITION PUBLICATION ACTIONS
# ==========================================================

@admin.action(description="Publish selected competitions")
def publish_competitions(modeladmin, request, queryset):

    updated = queryset.update(
        publication_status="published",
        published_by=request.user,
        published_at=timezone.now(),
    )

    modeladmin.message_user(
        request,
        f"{updated} competition(s) published successfully.",
        messages.SUCCESS,
    )


@admin.action(description="Move selected competitions to review")
def submit_competitions_for_review(
    modeladmin,
    request,
    queryset,
):

    updated = queryset.update(
        publication_status="pending_review",
    )

    modeladmin.message_user(
        request,
        f"{updated} competition(s) moved to review.",
        messages.INFO,
    )


@admin.action(description="Archive selected competitions")
def archive_competitions(
    modeladmin,
    request,
    queryset,
):

    updated = queryset.update(
        publication_status="archived",
    )

    modeladmin.message_user(
        request,
        f"{updated} competition(s) archived.",
        messages.WARNING,
    )


# ==========================================================
# COMPETITION ADMIN
# ==========================================================

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "organizer",
        "publication_status",
        "featured",
        "registration_deadline",
        "competition_date",
        "published_at",
    )

    list_filter = (
        "publication_status",
        "category",
        "featured",
    )

    search_fields = (
        "name",
        "category",
        "organizer",
        "organizing_institution",
        "official_source",
        "description",
    )

    list_editable = (
        "featured",
    )

    readonly_fields = (
        "published_by",
        "published_at",
        "created_at",
        "updated_at",
    )

    date_hierarchy = "competition_date"

    ordering = (
        "-featured",
        "-competition_date",
        "-created_at",
    )

    actions = (
        publish_competitions,
        submit_competitions_for_review,
        archive_competitions,
    )

    inlines = (
        CompetitionGalleryInline,
        CompetitionDocumentInline,
        SchoolCompetitionInline,
    )

    fieldsets = (

        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "category",
                    "description",
                    "image",
                    "featured",
                )
            },
        ),

        (
            "Organizer & Official Source",
            {
                "fields": (
                    "organizer",
                    "organizing_institution",
                    "official_source",
                )
            },
        ),

        (
            "Eligibility & Learning Areas",
            {
                "fields": (
                    "eligibility",
                    "target_level",
                    "subjects_skills",
                )
            },
        ),

        (
            "Dates & Location",
            {
                "fields": (
                    "registration_deadline",
                    "competition_date",
                    "location",
                )
            },
        ),

        (
            "Registration",
            {
                "fields": (
                    "registration_info",
                    "registration_link",
                )
            },
        ),

        (
            "Contact & Official Website",
            {
                "fields": (
                    "contact_email",
                    "contact_phone",
                    "website",
                )
            },
        ),

        (
            "Rules & Prizes",
            {
                "fields": (
                    "rules",
                    "prizes",
                )
            },
        ),

        (
            "Publication",
            {
                "fields": (
                    "publication_status",
                    "published_by",
                    "published_at",
                )
            },
        ),

        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


# ==========================================================
# SCHOOL COMPETITION / RESULTS
# ==========================================================

@admin.register(SchoolCompetition)
class SchoolCompetitionAdmin(admin.ModelAdmin):

    list_display = (
        "competition",
        "school",
        "year",
        "position",
        "achievement",
    )

    list_filter = (
        "year",
        "competition",
    )

    search_fields = (
        "competition__name",
        "school__name",
        "achievement",
    )

    ordering = (
        "-year",
        "position",
    )


# ==========================================================
# CAREERS
# ==========================================================

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
    )

    list_filter = (
        "category",
    )

    search_fields = (
        "name",
        "category",
    )


# ==========================================================
# TVET PROGRAMS
# ==========================================================

@admin.register(TVETProgram)
class TVETProgramAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "institution",
        "category",
        "duration",
    )

    list_filter = (
        "category",
    )

    search_fields = (
        "name",
        "institution",
        "category",
    )


# ==========================================================
# SCHOOL ACTIVITIES / EVENTS
# ==========================================================

@admin.register(SchoolActivity)
class SchoolActivityAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "school",
        "activity_date",
        "is_published",
        "created_at",
    )

    list_filter = (
        "is_published",
        "activity_date",
        "school",
    )

    search_fields = (
        "title",
        "school__name",
        "description",
    )

    ordering = (
        "-activity_date",
        "-created_at",
    )
# ==========================================================
# OPPORTUNITIES
# ==========================================================

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "organization",
        "category",
        "deadline",
        "is_featured",
        "is_published",
        "created_at",
    )

    search_fields = (
        "title",
        "organization",
        "description",
        "eligibility",
    )

    list_filter = (
        "category",
        "is_featured",
        "is_published",
        "deadline",
    )

    ordering = (
        "-is_featured",
        "deadline",
        "-created_at",
    )

    fieldsets = (
        (
            "Opportunity Information",
            {
                "fields": (
                    "title",
                    "organization",
                    "category",
                    "description",
                    "eligibility",
                )
            },
        ),
        (
            "Application",
            {
                "fields": (
                    "deadline",
                    "application_url",
                )
            },
        ),
        (
            "Presentation",
            {
                "fields": (
                    "image",
                    "is_featured",
                    "is_published",
                )
            },
        ),
    )    
