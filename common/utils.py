from datetime import date, datetime
import inspect
from datetime import datetime
from django.apps import apps
from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import models
from django.forms import Textarea
from django.core.exceptions import ValidationError
import os
import magic

from PIL import Image

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
        raise RuntimeError(
            f"Could not determine app for module {current_module.__name__}")

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


def validate_maximum_size(width=None, height=None):
    # https://odwyer.software/blog/how-to-validate-django-imagefield-dimensions
    # does not work - receive error ValueError: Could not find function validator in common.utils.
    def validator(image):
        error = False
        if width is not None and image.width > width:
            error = True
        if height is not None and image.height > height:
            error = True
        if error:
            raise ValidationError(
                [f'Size should be less than {width} x {height} pixels.']
            )

    return validator


# def validate_favicon(file):
#     # https://stackoverflow.com/questions/3648421/only-accept-a-certain-file-type-in-filefield-server-side
#     valid_mime_types = {
#         '.ico': 'image/x-icon',
#         '.png': 'image/png',
#         '.svg': 'image/svg+xml',
#     }
#     valid_sizes = [(16, 16), (32, 32), (64, 64)]

#     ext = os.path.splitext(file.name.lower())[1]
#     if ext not in valid_mime_types:
#         raise ValidationError(
#             'Invalid file extension. Allowed: .ico, .png, .svg')

#     mime_type = magic.from_buffer(file.read(2048), mime=True)
#     file.seek(0)

#     if mime_type != valid_mime_types[ext]:
#         raise ValidationError('Unsupported file type. Must be ICON, PNG or SVG')

#     if ext in ['.ico', '.png']:
#         img = Image.open(file)
#         if img.size not in valid_sizes:
#             raise ValidationError('Image must be 16x16, 32x32, or 64x64.')
#         file.seek(0)

def validate_favicon(image):
    allowed_mime_type = 'image/png'
    allowed_sizes = [(32, 32), (64, 64)]

    if not image.name.lower().endswith('.png'):
        raise ValidationError('Only PNG files are allowed.')

    mime_type = magic.from_buffer(image.read(2048), mime=True)
    image.seek(0)
    if mime_type != allowed_mime_type:
        raise ValidationError('File content must be a valid PNG image.')

    img = Image.open(image)
    if img.size not in allowed_sizes:
        raise ValidationError('Favicon must be exactly 32x32 or 64x64 pixels.')



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
