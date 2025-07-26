from django.apps import apps
from django.contrib import admin
from django.db import models


from common.utils import FormOverridesMixin, ListDisplayMixin, register_current_app_models
from core.models import Basics, Highlight, Job, Keyword, Skill
from common.singleton import SingletonModelAdmin

# NOTE: for import/export: use Django dumpdata/loaddata or via database
# NOTE: mixin before the ModelAdmin


@admin.register(Basics)
class BasicsAdmin(SingletonModelAdmin):
    pass


class HighlightInline(FormOverridesMixin, admin.TabularInline):
    model = Highlight
    extra = 0

    class Media:
        css = {
            "all": ["admin/inline.css"],
        }


class KeywordInline(FormOverridesMixin, admin.TabularInline):
    model = Keyword
    extra = 0

    class Media:
        css = {
            "all": ["admin/inline.css"],
        }


@admin.register(Skill)
class SkillAdmin(FormOverridesMixin, admin.ModelAdmin):
    # This just works - keywords are automatically filtered
    inlines = [KeywordInline]

    def get_keywords(self, obj):
        return ", ".join([
            keyword.name for keyword in obj.keywords.all()
        ])
    get_keywords.short_description = "Keywords"

    list_display = ['name', 'get_keywords']
    list_display_links = ['name', 'get_keywords']


@admin.register(Job)
class JobAdmin(FormOverridesMixin, ListDisplayMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                ('position'),
                ('summary'),
                ('org', 'client'),
                ('address'),
                ('start_date', 'end_date', 'is_current_position'),
                ('salary_from', 'salary_to', 'salary_per'),
                ('location_type', 'employment_type'),
                ('reason_for_leaving', 'okay_to_contact')
            ),
        }),
    )
    inlines = [HighlightInline]

    #TODO reuse this for education, need to order educ fields in admin
    class Media:
        css = {
            "all": ["admin/core/css/main.css"],

        }
        js = ["admin/core/js/job_admin.js"]


# Call the function after registering any specific model admin class.
register_current_app_models()
