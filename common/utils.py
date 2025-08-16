from datetime import date, datetime
import inspect
from datetime import datetime
from django.apps import apps
from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.db import models
from django.forms import Textarea

#TODO remove unused imports

'''
    HELPERS
'''
# https://stackoverflow.com/questions/10543032/how-to-show-all-model-fields-in-the-admin-page


def get_registered_inline_models():
    """
    Find all model classes used in registered inline admin classes.
    """
    inline_models = set()

    # Check all admin classes registered so far
    for model, admin_class in admin.site._registry.items():
        # ignore model not accessed - everything works
        for inline in getattr(admin_class, 'inlines', []):
            # Inline can be a class or instance — normalize
            inline_class = inline if inspect.isclass(
                inline) else inline.__class__

            if issubclass(inline_class, InlineModelAdmin):
                try:
                    inline_model = inline_class.model
                    if inline_model:
                        inline_models.add(inline_model)
                except AttributeError:
                    pass

    return inline_models


def register_current_app_models():
    """
      automatically register models
      https://tomdekan.com/articles/automatically-register-django-admin-models      
    """
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

    current_module = inspect.getmodule(inspect.stack()[1][0])
    app_config = apps.get_containing_app_config(current_module.__name__)
    if not app_config:
        raise RuntimeError(f"Could not determine app for module {current_module.__name__}")

    inline_models = get_registered_inline_models()
    app_models = app_config.get_models()

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


def format_date_display(value, date_label="Present"):
    if value is None:
        return date_label

    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value)
        except ValueError:
            return value  # return as-is if not parseable

    if isinstance(value, (date, datetime)):
        return value.strftime('%b %Y')

    return ''


'''
    MIXINS
'''


class FormOverridesMixin:
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 75})},
    }


class AdminMediaMixin:
    class Media:
        css = {
            "all": ["admin/css/toggle_end_date.css"],

        }
        js = ["admin/js/toggle_end_date.js", "admin/js/validate_iso_date.js"]


class ListDisplayMixin:
    def __init__(self, model, admin_site):
        self.list_display = [
            field.name for field in model._meta.fields if field.name != "id"]
        self.list_display_links = [
            field.name for field in model._meta.fields if field.name != "id"
        ]
        super(ListDisplayMixin, self).__init__(model, admin_site)


class FormatDatesMixin(models.Model):
    class Meta:
        # prevent db table from being created
        abstract = True

    @property
    def start_date_formatted(self):
        return format_date_display(self.start_date, date_label="")

    @property
    def end_date_formatted(self):
        return format_date_display(self.end_date)


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


class ReadOnlyAdminMixin:
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class StaffRequiredMixin(LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'is_staff'
