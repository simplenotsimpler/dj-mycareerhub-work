from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

from core.models import Basics, Education, Job, Keyword, SocialProfile

'''
  NOTE: models originally developed in the dj-mch-test-resume repo
'''


class Resume(models.Model):
    # TODO maybe make name unique?? at very least need show id in the admin
    name = models.CharField(max_length=125, default='resume')
    professional_profile = models.TextField(null=True, blank=True)
    is_public = models.BooleanField(default=False)
    # Okay to set default to 1 since we are using a singleton & this will be read only in the admin
    # https://www.geeksforgeeks.org/python/setting-default-value-for-foreign-key-attribute-in-django/
    basics = models.ForeignKey(
        Basics, on_delete=models.SET_NULL, null=True, default=1, related_name='resumes')
    social_profiles = models.ManyToManyField(
        SocialProfile,
        blank=True
    )
    # skills pulled in via keywords
    keywords = models.ManyToManyField(
        Keyword,
        blank=True
    )
    jobs = models.ManyToManyField(
        Job,
        blank=True
    )

    educations = models.ManyToManyField(
        Education,
        blank=True
    )

    def __str__(self):
        return self.name or f'Resume {self.pk}'

    # https://www.abidibo.net/blog/2015/01/21/add-links-django-admin-changelist-view/
    def print_link(self):
        return mark_safe('<a class="grp-button" href="%s" target="blank">Print view</a>' % reverse('resume_detail', args=[self.id]))
    print_link.short_description = "Print view"

    def word_link(self):
        return mark_safe('<a class="grp-button" href="%s" target="blank">Word doc</a>' % reverse('get_word_with_pk', args=[self.id]))
    word_link.short_description = "Word doc"
