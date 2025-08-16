from datetime import date
from django.db import models
from dateutil.relativedelta import relativedelta
from django.db.models import Q


from core.models import Contact, Education, Job

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

class WorkHistory(Job):
    class Meta:
        proxy = True
        verbose_name = "Work History"
        verbose_name_plural = "Work History"

    class WorkHistoryReportManager(models.Manager):
        def get_queryset(self) -> models.QuerySet:
            return super().get_queryset().order_by('-end_date', '-start_date')

    objects = WorkHistoryReportManager()

class ContactList(Contact):
    class Meta:
        proxy = True
        verbose_name = "Contact List"
        verbose_name_plural = "Contact List"

    class ContactListReportManager(models.Manager):
        def get_queryset(self) -> models.QuerySet:
            return super().get_queryset().filter(Q(current_reference=True) | Q(background_check=True))

    objects = ContactListReportManager()

    @property
    def how_long_known(self):
        duration = relativedelta(date.today(), self.known_since)
        # {duration.years} Years {duration.months} months {duration.days} days
        output = f'{duration.years} Years'
        return output
