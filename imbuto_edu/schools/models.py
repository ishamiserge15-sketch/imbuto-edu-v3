from django.db import models
from django.contrib.auth.models import User


# ============================================================
# SCHOOL MODEL
# ============================================================

class School(models.Model):

    SCHOOL_TYPES = [
        ("Boarding", "Boarding"),
        ("Day", "Day"),
        ("Mixed", "Mixed"),
    ]

    OWNERSHIP_CHOICES = [
        ("Government", "Government"),
        ("Private", "Private"),
        ("Faith-Based", "Faith-Based"),
    ]

    # --------------------------------------------------------
    # BASIC INFORMATION
    # --------------------------------------------------------

    name = models.CharField(
        max_length=200
    )

    district = models.CharField(
        max_length=100
    )

    province = models.CharField(
        max_length=100
    )

    category = models.CharField(
        max_length=100
    )

    school_type = models.CharField(
        max_length=20,
        choices=SCHOOL_TYPES
    )

    ownership = models.CharField(
        max_length=30,
        choices=OWNERSHIP_CHOICES
    )

    # --------------------------------------------------------
    # CONTACT
    # --------------------------------------------------------

    school_fees = models.CharField(
        max_length=100,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    website = models.URLField(
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # IMAGE
    # --------------------------------------------------------

    image = models.ImageField(
        upload_to="schools/",
        blank=True,
        null=True
    )

    # --------------------------------------------------------
    # EDUCATIONAL INFORMATION
    # --------------------------------------------------------

    facilities = models.TextField(
        blank=True
    )

    subjects = models.TextField(
        blank=True
    )

    academic_performance = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # RANKING
    # --------------------------------------------------------

    academic_score = models.PositiveIntegerField(
        default=0
    )

    sports_score = models.PositiveIntegerField(
        default=0
    )

    innovation_score = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return self.name


# ============================================================
# SPORT
# ============================================================

class Sport(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to="sports/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


# ============================================================
# SCHOOL SPORT
# ============================================================

class SchoolSport(models.Model):

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="sports"
    )

    sport = models.ForeignKey(
        Sport,
        on_delete=models.CASCADE,
        related_name="schools"
    )

    achievement = models.TextField(
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.school.name} - {self.sport.name}"


# ============================================================
# COMPETITION
# ============================================================

class Competition(models.Model):

    PUBLICATION_STATUS = [
        ("draft", "Draft"),
        ("pending_review", "Pending Review"),
        ("published", "Published"),
        ("archived", "Archived"),
    ]

    # --------------------------------------------------------
    # BASIC INFORMATION
    # --------------------------------------------------------

    name = models.CharField(
        max_length=200
    )

    category = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to="competitions/",
        blank=True,
        null=True
    )

    # --------------------------------------------------------
    # ORGANIZATION / AUTHORITY
    # --------------------------------------------------------

    organizer = models.CharField(
        max_length=200,
        blank=True
    )

    organizing_institution = models.CharField(
        max_length=200,
        blank=True
    )

    official_source = models.CharField(
        max_length=300,
        blank=True,
        help_text=(
            "Official institution or authority responsible "
            "for this competition."
        )
    )

    # --------------------------------------------------------
    # ELIGIBILITY / EDUCATION
    # --------------------------------------------------------

    eligibility = models.TextField(
        blank=True
    )

    target_level = models.CharField(
        max_length=200,
        blank=True,
        help_text=(
            "Example: Primary, Lower Secondary, "
            "Upper Secondary, TVET."
        )
    )

    subjects_skills = models.TextField(
        blank=True,
        help_text=(
            "Subjects, skills or areas covered by "
            "the competition."
        )
    )

    # --------------------------------------------------------
    # DATES / LOCATION
    # --------------------------------------------------------

    registration_deadline = models.DateField(
        blank=True,
        null=True
    )

    competition_date = models.DateField(
        blank=True,
        null=True
    )

    location = models.CharField(
        max_length=300,
        blank=True
    )

    # --------------------------------------------------------
    # REGISTRATION
    # --------------------------------------------------------

    registration_info = models.TextField(
        blank=True
    )

    registration_link = models.URLField(
        blank=True
    )

    # --------------------------------------------------------
    # CONTACT
    # --------------------------------------------------------

    contact_email = models.EmailField(
        blank=True
    )

    contact_phone = models.CharField(
        max_length=50,
        blank=True
    )

    # --------------------------------------------------------
    # RULES / PRIZES
    # --------------------------------------------------------

    rules = models.TextField(
        blank=True
    )

    prizes = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # OFFICIAL WEBSITE
    # --------------------------------------------------------

    website = models.URLField(
        blank=True
    )

    # --------------------------------------------------------
    # PUBLICATION / ADMINISTRATION
    # --------------------------------------------------------

    publication_status = models.CharField(
        max_length=30,
        choices=PUBLICATION_STATUS,
        default="published"
    )

    featured = models.BooleanField(
        default=False
    )

    published_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="published_competitions"
    )

    published_at = models.DateTimeField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


# ============================================================
# SCHOOL COMPETITION
# ============================================================

class SchoolCompetition(models.Model):

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="competitions"
    )

    competition = models.ForeignKey(
        Competition,
        on_delete=models.CASCADE,
        related_name="participating_schools"
    )

    year = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    position = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    achievement = models.TextField(
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.school.name} - {self.competition.name}"


# ============================================================
# CAREER
# ============================================================

class Career(models.Model):

    name = models.CharField(
        max_length=200
    )

    category = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    subjects = models.TextField(
        blank=True,
        help_text="Recommended subjects or school subjects."
    )

    skills = models.TextField(
        blank=True,
        help_text="Important skills for this career."
    )

    image = models.ImageField(
        upload_to="careers/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


# ============================================================
# TVET PROGRAM
# ============================================================

class TVETProgram(models.Model):

    name = models.CharField(
        max_length=200
    )

    institution = models.CharField(
        max_length=200,
        blank=True
    )

    category = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    entry_requirements = models.TextField(
        blank=True
    )

    duration = models.CharField(
        max_length=100,
        blank=True
    )

    image = models.ImageField(
        upload_to="tvet/",
        blank=True,
        null=True
    )

    website = models.URLField(
        blank=True
    )

    def __str__(self):
        return self.name


# ============================================================
# SCHOOL ACCOUNT
# ============================================================

class SchoolAccount(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending Verification"),
        ("verified", "Verified"),
        ("rejected", "Rejected"),
        ("suspended", "Suspended"),
    ]

    school = models.OneToOneField(
        School,
        on_delete=models.CASCADE,
        related_name="account",
    )

    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="school_account",
    )

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.school.name} Account"


# ============================================================
# SCHOOL VERIFICATION
# ============================================================

class SchoolVerification(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending Review"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("needs_update", "Needs Update"),
    ]

    school = models.OneToOneField(
        School,
        on_delete=models.CASCADE,
        related_name="verification",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True,
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    reviewer_notes = models.TextField(
        blank=True,
    )

    def __str__(self):
        return f"{self.school.name} Verification"


# ============================================================
# SCHOOL REGISTRATION REQUEST
# ============================================================

class SchoolRegistrationRequest(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending Review"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    school_name = models.CharField(
        max_length=200
    )

    district = models.CharField(
        max_length=100
    )

    province = models.CharField(
        max_length=100
    )

    school_type = models.CharField(
        max_length=100
    )

    ownership = models.CharField(
        max_length=100
    )

    contact_person = models.CharField(
        max_length=150
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=30
    )

    website = models.URLField(
        blank=True
    )

    message = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    admin_notes = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.school_name} - Registration Request"


# ============================================================
# SCHOOL ACTIVITY
# ============================================================

class SchoolActivity(models.Model):

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="activities"
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    image = models.ImageField(
        upload_to="school_activities/",
        blank=True,
        null=True,
    )

    activity_date = models.DateField(
        blank=True,
        null=True,
    )

    is_published = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.school.name} - {self.title}"


# ============================================================
# COMPETITION GALLERY
# ============================================================

class CompetitionGallery(models.Model):

    competition = models.ForeignKey(
        Competition,
        on_delete=models.CASCADE,
        related_name="gallery"
    )

    image = models.ImageField(
        upload_to="competition_gallery/"
    )

    caption = models.CharField(
        max_length=200,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.competition.name} Gallery Image"


# ============================================================
# COMPETITION DOCUMENT
# ============================================================

class CompetitionDocument(models.Model):

    competition = models.ForeignKey(
        Competition,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    title = models.CharField(
        max_length=200
    )

    document = models.FileField(
        upload_to="competition_documents/"
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.competition.name} - {self.title}"
# ==========================================================
# OPPORTUNITIES
# ==========================================================

class Opportunity(models.Model):

    CATEGORY_CHOICES = [
        ("Scholarship", "Scholarship"),
        ("Leadership", "Leadership"),
        ("STEM", "STEM"),
        ("Exchange", "Exchange Program"),
        ("Competition", "Competition"),
        ("Government", "Government Opportunity"),
        ("TVET", "TVET Opportunity"),
        ("University", "University Opportunity"),
        ("Youth", "Youth Program"),
        ("Other", "Other"),
    ]

    title = models.CharField(
        max_length=250
    )

    organization = models.CharField(
        max_length=200
    )

    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES
    )

    description = models.TextField()

    eligibility = models.TextField(
        blank=True
    )

    deadline = models.DateField(
        blank=True,
        null=True
    )

    application_url = models.URLField(
        blank=True
    )

    image = models.ImageField(
        upload_to="opportunities/",
        blank=True,
        null=True
    )

    is_published = models.BooleanField(
        default=False
    )

    is_featured = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title    