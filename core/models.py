from collections import defaultdict
from djmoney.models.fields import MoneyField
from django.db import models
from common.singleton import *
from common.utils import FormatDatesMixin, TitleCaseFieldsMixin

# NOTE: on_delete only set in db for CASCADE, not other options
# See https://docs.djangoproject.com/en/5.2/ref/models/fields/#django.db.models.ForeignKey
# See https://code.djangoproject.com/ticket/21961


class Address(models.Model):
    address_line_1 = models.CharField(max_length=45)
    address_line_2 = models.CharField(max_length=45, blank=True, null=True)
    address_line_3 = models.CharField(max_length=45, blank=True, null=True)
    city = models.CharField(max_length=45, blank=True, null=True)
    region = models.CharField(max_length=45, blank=True, null=True)
    postal_code = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return self.address_line_1

    @property
    def city_region(self):
        return f"{self.city}, {self.region}"


class ContactRelationship(TitleCaseFieldsMixin):
    description = models.CharField(max_length=45)
    title_case_fields = ['description']

    class Meta:
        verbose_name = "Contact Relationship"
        verbose_name_plural = "Contact Relationships"

    def __str__(self):
        # NOTE: admin changelist requires overriding in list_display to see title case
        return self.description.title() if self.description else ""


class Contact(models.Model):
    full_name = models.CharField(max_length=125)
    position = models.CharField(blank=True, null=True, max_length=125)
    org = models.ForeignKey(
        "Organization",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Organization"
    )
    phone = models.CharField(blank=True, null=True, max_length=125)
    fax = models.CharField(blank=True, null=True, max_length=125)
    email = models.CharField(blank=True, null=True, max_length=255)
    linkedin = models.CharField(
        blank=True, null=True, verbose_name="LinkedIn", max_length=255)
    known_since = models.DateField(default=None, blank=True, null=True)
    referral_org = models.ForeignKey(
        "Organization",
        on_delete=models.SET_NULL,
        related_name="contact_known_from_org_set",
        blank=True,
        null=True,
        verbose_name="Where met?"
    )
    relationship = models.ForeignKey(
        "ContactRelationship", on_delete=models.SET_NULL, blank=True, null=True)
    relationship_is_former = models.BooleanField(
        verbose_name="Former relationship?", default=False)
    current_reference = models.BooleanField(
        verbose_name="Current reference?", default=False)
    background_check = models.BooleanField(
        verbose_name="For background check?", default=False)
    notes = models.TextField(blank=True, null=True, max_length=250)

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return self.full_name


class Education(FormatDatesMixin, models.Model):
    institution = models.ForeignKey(
        "Organization", on_delete=models.SET_NULL, blank=True, null=True
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Institution Address",
    )
    degree = models.CharField(max_length=125)
    field_of_study = models.CharField(blank=True, null=True, max_length=125)
    concentration = models.CharField(blank=True, null=True, max_length=125)
    start_date = models.DateField(default=None, blank=True, null=True)
    end_date = models.DateField(default=None, blank=True, null=True)
    note = models.TextField(blank=True, null=True, max_length=250)
    score = models.FloatField(blank=True, null=True)
    scale = models.FloatField(blank=True, null=True, default=4.0)
    courses_only = models.BooleanField(
        verbose_name="Courses only?", default=False)
    is_current = models.BooleanField(
        verbose_name="Currently attend here", default=False
    )

    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Education"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(end_date__gt=models.F("start_date")),
                name="check_start_date_educ",
                violation_error_message="End date must be after start date",
            ),
        ]

    def __str__(self):
        return f"{self.degree} - {self.field_of_study} - {self.institution}"

    @property
    def location(self):
        # encapsulate this return so can easily display in reports admin, etc.
        return self.address.city_region

    @property
    def gpa(self):
        return f"{self.score} / {self.scale}"

    @property
    def degree_field(self):
        return f"{self.degree}, {self.field_of_study}"

    degree_field.fget.short_description = u'Degree'


class EmploymentType(TitleCaseFieldsMixin):
    emp_type = models.CharField(max_length=45)
    title_case_fields = ['emp_type']

    class Meta:
        verbose_name = "Employment Type"
        verbose_name_plural = "Employment Types"

    def __str__(self):
        # NOTE: admin changelist requires overriding in list_display to see title case
        return self.emp_type.title() if self.emp_type else ""


class Highlight(models.Model):
    highlight_text = models.TextField(blank=True, null=True, max_length=125)
    job = models.ForeignKey(
        "Job", on_delete=models.SET_NULL, blank=True, null=True, related_name="highlights")
    is_duty = models.BooleanField(verbose_name="Is duty?", default=False)

    class Meta:
        verbose_name = "Highlight"
        verbose_name_plural = "Highlights"

    def __str__(self):
        return self.highlight_text


class SalaryType(TitleCaseFieldsMixin):
    name = models.CharField(max_length=50)
    title_case_fields = ['name']

    class Meta:
        managed = True
        verbose_name = "Salary Type"
        verbose_name_plural = "Salary Types"

    def __str__(self):
        # NOTE: admin changelist requires overriding in list_display to see title case
        return self.name.title() if self.name else ""


class LocationType(TitleCaseFieldsMixin):
    name = models.CharField(max_length=50)
    title_case_fields = ['name']

    class Meta:
        verbose_name = "Location Type"
        verbose_name_plural = "Location Types"

    def __str__(self):
        # NOTE: admin changelist requires overriding in list_display to see title case
        return self.name.title() if self.name else ""


class Job(FormatDatesMixin, models.Model):
  # NOTE: reordering fields here does not change order in the db
  # No migration needed but does update the admin order    
    position = models.CharField(
        max_length=125, help_text="Official position title")
    position_supplement = models.CharField(
        blank=True, null=True, max_length=125, help_text="Used when official position title not clear")
    # summary per JSONResume summary
    summary = models.TextField(blank=True, null=True, max_length=250)
    org = models.ForeignKey(
        "Organization",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="job_org",
        verbose_name="Organization",
    )
    client = models.ForeignKey(
        "Organization",
        on_delete=models.SET_NULL,
        related_name="job_client",
        blank=True,
        null=True
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="job_address",
        verbose_name="Position Address"
    )
    employment_type = models.ForeignKey(
        EmploymentType, on_delete=models.SET_DEFAULT, default=1, related_name="job_emptype"
    )
    start_date = models.DateField(default=None, blank=True, null=True)
    end_date = models.DateField(default=None, blank=True, null=True)
    is_current = models.BooleanField(
        verbose_name="I currently work here", default=False
    )

    salary_from = MoneyField(
        max_digits=14, decimal_places=2, default_currency="USD", blank=True, null=True
    )
    salary_to = MoneyField(
        max_digits=14, decimal_places=2, default_currency="USD", blank=True, null=True
    )

    salary_per = models.ForeignKey(
        SalaryType, on_delete=models.SET_NULL, blank=True, null=True, default=1
    )
    location_type = models.ForeignKey(
        LocationType, on_delete=models.SET_NULL, blank=True, null=True, default=1
    )
    reason_for_leaving = models.CharField(
        blank=True, null=True, max_length=125)
    okay_to_contact = models.BooleanField(
        verbose_name="Okay to contact?", default=True)

    class Meta:
        managed = True
        verbose_name = "Job"
        verbose_name_plural = "Jobs"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(end_date__gt=models.F("start_date")),
                name="check_start_date",
                violation_error_message="End date must be after start date",
            ),
        ]

    def __str__(self):
        return f"{self.position} at {self.org}"

    @property
    def job_address(self):
        output = f"""
          {self.address.address_line_1}
          {self.address.address_line_2}
          {self.address.address_line_3}
          {self.address.city}, {self.address.region} {self.address.postal_code}
        """
        return output


class Organization(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=45, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Organization Address"
    )

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __str__(self):
        return self.name


class Basics(SingletonModel):
    # TODO: maybe refactor to user profile instead of singleton - so can follow principle of least privilege
    # NOTE: this is called Basics to align with JSON Resume standard
    full_name = models.CharField(blank=True, null=True, max_length=125)
    public_display_name = models.CharField(
        blank=True, null=True, max_length=125)
    website = models.CharField(blank=True, null=True, max_length=255)
    email = models.CharField(blank=True, null=True, max_length=255)
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, blank=True, null=True)
    phone = models.CharField(blank=True, null=True)

    class Meta:
        managed = True
        verbose_name = "Basics"
        verbose_name_plural = "Basics"

    def __str__(self):
        if self.full_name:
            return self.full_name
        else:
            return "New"


class Skill(models.Model):
    name = models.CharField(blank=True, null=True, max_length=125)

    # NOTE: added keywords here since the admin is using inlines and edits both
    class Meta:
        verbose_name = "Skills with keywords"
        verbose_name_plural = "Skills with keywords"

    def __str__(self):
        return self.name


class Keyword(models.Model):
    name = models.CharField(unique=True, max_length=45)
    skill = models.ForeignKey(
        "Skill", on_delete=models.SET_NULL, blank=True, null=True, related_name='keywords')

    class Meta:
        verbose_name = "Skill Keyword"
        verbose_name_plural = "Skill Keywords"

    # return skill for now until can group by keywords in admin
    def __str__(self):
        return f"{self.skill} - {self.name}"

    @classmethod
    def group_by_skill(cls, keywords_queryset):
        skill_keywords = defaultdict(list)

        # Only include keywords that are linked to a skill
        for keyword in keywords_queryset.filter(skill__isnull=False).select_related('skill'):
            skill_keywords[keyword.skill.name].append(keyword.name)

        # Convert defaultdict to a regular dictionary and return
        return dict(skill_keywords)


class SocialProfile(models.Model):
    basics = models.ForeignKey(
        Basics, on_delete=models.SET_NULL, blank=True, null=True, related_name="socials")
    network = models.CharField(max_length=45, blank=True, null=True)
    username = models.CharField(max_length=45, blank=True, null=True)
    url = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Social Profile"
        verbose_name_plural = "Social Profiles"

    def __str__(self):
        return f"{self.network} - {self.username}"
