import inspect
from django.contrib.admin.options import InlineModelAdmin
from django.apps import apps
from django.contrib import admin
from django.db import models
from django.forms import Textarea

from core.models import Basics, Highlight, Job, Keyword, Skill
from core.singleton import SingletonModelAdmin

# NOTE: for import/export: use Django dumpdata/loaddata or via database
# NOTE: mixin before the ModelAdmin


class FormOverridesMixin:
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 75})},
    }

# https://stackoverflow.com/questions/10543032/how-to-show-all-model-fields-in-the-admin-page


class ListDisplayMixin:
    def __init__(self, model, admin_site):
        self.list_display = [
            field.name for field in model._meta.fields if field.name != "id"]
        self.list_display_links = [
            field.name for field in model._meta.fields if field.name != "id"
        ]
        super(ListDisplayMixin, self).__init__(model, admin_site)

def get_registered_inline_models():
    """
    Find all model classes used in registered inline admin classes.
    """
    inline_models = set()

    # Check all admin classes registered so far
    for model, admin_class in admin.site._registry.items():
        for inline in getattr(admin_class, 'inlines', []):
            # Inline can be a class or instance — normalize
            inline_class = inline if inspect.isclass(inline) else inline.__class__

            if issubclass(inline_class, InlineModelAdmin):
                try:
                    inline_model = inline_class.model
                    if inline_model:
                        inline_models.add(inline_model)
                except AttributeError:
                    pass

    return inline_models        

# TODO move comment into the function so closer to code
# automatically register models
# https://tomdekan.com/articles/automatically-register-django-admin-models


# only register core apps so do not have to unregister in other admin pages
def register_current_app_models():
    """
    Register any unregistered app models. We call this function    after registering any custom admin classes.
     """
    models_to_ignore = [
        'admin.LogEntry',
        'contenttypes.ContentType',
        'sessions.Session',
        'authtoken.TokenProxy',
        # We automatically register the authtoken app models.
        'authtoken.Token',
    ]

    inline_models = get_registered_inline_models()
    app_models = apps.get_app_config('core').get_models()
    # for model in apps.get_models():
    for model in app_models:
        try:
            # if model._meta.label in models_to_ignore:
            if (
                model._meta.label in models_to_ignore or
                model in inline_models
            ):
                continue
            else:
                class modelAdmin(FormOverridesMixin, ListDisplayMixin, admin.ModelAdmin):
                    pass
                    ordering = ('id',)

                admin.site.register(model, modelAdmin)
        except admin.sites.AlreadyRegistered:
            pass


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

    # list_display = ['name', 'icon', 'get_keywords']
    list_display = ['name', 'icon', 'get_keywords']
    list_display_links = ['name', 'icon', 'get_keywords']


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

    class Media:
        css = {
            "all": ["admin/core/css/main.css"],

        }
        js = ["admin/core/js/job_admin.js"]


# Call the function after registering any specific model admin class.
register_current_app_models()
