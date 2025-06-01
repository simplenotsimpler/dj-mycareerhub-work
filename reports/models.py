from datetime import date
from django.db import models
# from dateutil import relativedelta
from dateutil.relativedelta import relativedelta


from core.models import Contact, Education, Job


class ContactPropertiesMixin:
    @property
    def how_long_known(self):
        duration = relativedelta(date.today(), self.known_since)
        # {duration.years} Years {duration.months} months {duration.days} days
        output = f'{duration.years} Years'
        return output

    # line breaks not working in f string
    # maybe use later
    @property
    def known_and_duration(self):
        output = f"""
          {self.known_since.strftime("%b %Y")}
          {self.how_long_known}
        """
        return output

# https://micropyramid.com/blog/overriding-django-model-behaviour-with-proxy-model/
# https://www.youtube.com/watch?v=KF2p-LQjZZ4


class EducHistory(Education):
    class Meta:
        proxy = True
        verbose_name = "Education History"
        verbose_name_plural = "Education History"

    class EducHistoryReportManager(models.Manager):
        def get_queryset(self) -> models.QuerySet:
            return super().get_queryset().exclude(courses_only=True).order_by('-end_date', '-start_date')

    objects = EducHistoryReportManager()

    def __str__(self):
        return self.degree

    @property
    def degree_field(self):
        return f"{self.degree}, {self.field_of_study}"

    degree_field.fget.short_description = u'Degree'

    @property
    def location(self):
        return f"{self.address.city}, {self.address.region}"

    @property
    def start_to_end(self):
        return f"{self.start_date.strftime("%b %Y")} - {self.end_date.strftime("%b %Y")}"

    @property
    def gpa(self):
        return f"{self.score} / {self.scale}"


class WorkHistory(Job):
    class Meta:
        proxy = True
        verbose_name = "Work History"
        verbose_name_plural = "Work History"

    class WorkHistoryReportManager(models.Manager):
        def get_queryset(self) -> models.QuerySet:
            return super().get_queryset().order_by('-end_date', '-start_date')

    objects = WorkHistoryReportManager()

    def __str__(self):
        return f"{self.position} at {self.org}"

    @property
    def end_date_or_present(self):
        return "Present" if not self.end_date else self.end_date
        # return f"{self.start_date} - {end_date_or_present}"
        # return f"{self.start_date.strftime("%b %Y")} - {self.end_date.strftime("%b %Y")}"

    @property
    def job_address(self):
        output = f"""
          {self.address.address_line_1}
          {self.address.address_line_2}
          {self.address.address_line_3}
          {self.address.city}, {self.address.region} {self.address.postal_code}
        """
        return output


class ContactReferences(ContactPropertiesMixin, Contact):
    class Meta:
        proxy = True
        verbose_name = "Contact References"
        verbose_name_plural = "Contact References"

    class ContactReferencesReportManager(models.Manager):
        def get_queryset(self) -> models.QuerySet:
            return super().get_queryset().filter(current_reference=True)

    objects = ContactReferencesReportManager()


class ContactBackgroundCheck(ContactPropertiesMixin, Contact):
    class Meta:
        proxy = True
        verbose_name = "Contact Background Check"
        verbose_name_plural = "Contact Background Check"

    class ContactReferencesReportManager(models.Manager):
        def get_queryset(self) -> models.QuerySet:
            return super().get_queryset().filter(current_reference=True, background_check=True)

    objects = ContactReferencesReportManager()
