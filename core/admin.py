from django.apps import apps
from django.contrib import admin
from django.db import models
from django.forms import Textarea

from core.models import Basics, Highlight, Job
from core.singleton import SingletonModelAdmin


# TODO: add Django import / export
# NOTE: >> may be part of custom admin theme

# TODO: customize admin >> either via theme or manually
# NOTE: no inlines until after theme / customization

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

    app_models = apps.get_app_config('core').get_models()
    # for model in apps.get_models():
    for model in app_models:
        try:
            if model._meta.label in models_to_ignore:
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


@admin.register(Job)
class JobAdmin(FormOverridesMixin, ListDisplayMixin, admin.ModelAdmin):
  # TODO: end_date read only if 'is_current_position' checked
  # can be done easily in Unfold theme
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

    # TODO: widen the position address width if adding theme does not fix
    # TODO: reduce distance b/n label and widget if adding them does not fix - maybe reduce gap on related-widget-wrapper
    class Media:
        css = {
            "all": ["admin/core/css/main.css"],

        }


# Call the function after registering any specific model admin class.
register_current_app_models()
