from djmoney.models.fields import MoneyField
from django.db import models
from .singleton import *

# TODO: add a config model via prebuilt singleton package
# TODO: also set FK on delete in db


class TitleCaseFieldsMixin(models.Model):
    # Ensure saved in title case in db
    title_case_fields = []  # List of field names to title-case

    def save(self, *args, **kwargs):
        for field in self.title_case_fields:
            value = getattr(self, field, None)
            if isinstance(value, str):
                setattr(self, field, value.title())
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Address(models.Model):
    address_line_1 = models.CharField(max_length=45, blank=True, null=True)
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


class ContactRelationship(TitleCaseFieldsMixin):
    description = models.CharField(max_length=45, blank=True, null=True)
    title_case_fields = ['description']

    class Meta:
        verbose_name = "Contact Relationship"
        verbose_name_plural = "Contact Relationships"

    def __str__(self):
        # NOTE: admin changelist requires overriding in list_display to see title case
        return self.description.title() if self.description else ""


class Contact(models.Model):
    full_name = models.CharField(blank=True, null=True, max_length=125)
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
    relationship_is_former=models.BooleanField(
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


class Education(models.Model):
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
    degree = models.CharField(blank=True, null=True, max_length=125)
    field_of_study = models.CharField(blank=True, null=True, max_length=125)
    concentration = models.CharField(blank=True, null=True, max_length=125)
    start_date = models.DateField(default=None, blank=True, null=True)
    end_date = models.DateField(default=None, blank=True, null=True)
    note = models.TextField(blank=True, null=True, max_length=250)
    score = models.FloatField(blank=True, null=True)
    scale = models.FloatField(blank=True, null=True, default=4.0)
    courses_only = models.BooleanField(
        verbose_name="Courses only?", default=False)

    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Education"

    def __str__(self):
        return f"{self.degree} - {self.field_of_study} - {self.institution}"


# class EmploymentType(models.Model):
class EmploymentType(TitleCaseFieldsMixin):
    emp_type = models.CharField(max_length=45, blank=True, null=True)
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
        "Job", on_delete=models.SET_NULL, blank=True, null=True, related_name="job_highlights")
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


class Job(models.Model):
  # NOTE: reordering fields here does not change order in the db
  # No migration needed but does update the admin order
    position = models.CharField(blank=True, null=True, max_length=125)
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
    is_current_position = models.BooleanField(
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
        return self.position


class Keyword(models.Model):
    name = models.CharField(unique=True, max_length=45, blank=True, null=True)
    skill = models.ForeignKey(
        "Skill", on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = "Skill Keyword"
        verbose_name_plural = "Skill Keywords"

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
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
    full_name = models.CharField(blank=True, null=True, max_length=125)
    display_name = models.CharField(blank=True, null=True, max_length=125)
    basics_website = models.CharField(blank=True, null=True, max_length=255)
    basics_email = models.CharField(blank=True, null=True, max_length=255)
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, blank=True, null=True)
    basics_phone = models.CharField(blank=True, null=True)

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
    icon = models.CharField(blank=True, null=True, max_length=125)

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def __str__(self):
        return self.name


class SocialProfile(models.Model):
    basics = models.ForeignKey(
        Basics, on_delete=models.SET_NULL, blank=True, null=True)
    network = models.CharField(max_length=45, blank=True, null=True)
    username = models.CharField(max_length=45, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Social Profile"
        verbose_name_plural = "Social Profiles"

    def __str__(self):
        return f"{self.network} - {self.username}"
