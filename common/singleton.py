
from django.contrib import admin, messages
from django.db import models
from django.http import HttpResponseRedirect
from django.urls import re_path, reverse
from django.utils.html import format_html
from urllib.parse import quote as urlquote

# https://medium.com/@akshatgadodia/leveraging-singleton-models-for-streamlined-django-administration-c678c546a28e

class SingletonModel(models.Model):
    singleton_instance_id = 1

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = self.singleton_instance_id
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=cls.singleton_instance_id)
        return obj

    @classmethod
    def get_field_value(cls, field_name, default_value=None):
        obj = cls.load()
        return getattr(obj, field_name, default_value)


class SingletonModelAdmin(admin.ModelAdmin):
    singleton_instance_id = 1

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_urls(self):
        """
        Overridden default get_urls to directly display change form instead of List Display
        """
        urls = super(SingletonModelAdmin, self).get_urls()
        model_name = self.model._meta.model_name

        url_name_prefix = '%(app_name)s_%(model_name)s' % {
            'app_name': self.model._meta.app_label,
            'model_name': model_name,
        }
        custom_urls = [
            re_path(r'^history/$',
                    self.admin_site.admin_view(self.history_view),
                    {'object_id': str(self.singleton_instance_id)},
                    name='%s_history' % url_name_prefix),
            re_path(r'^$',
                    self.admin_site.admin_view(self.change_view),
                    {'object_id': str(self.singleton_instance_id)},
                    name='%s_change' % url_name_prefix),
        ]

        return custom_urls + urls

    def response_change(self, request, obj):
        """
        Overridden default response_change to redirect to home page instead of list display page
        """

        # fix based on code in original:
        # https://github.com/django/django/blob/stable/5.2.x/django/contrib/admin/options.py
        msg_dict = {
            "name": self.opts.verbose_name,
            "obj": format_html('<a href="{}">{}</a>', urlquote(request.path), obj),
        }
        msg = format_html(
            ("The {name} “{obj}” was changed successfully."), **msg_dict
        )
        if '_continue' in request.POST:
            msg += format_html('  You may edit it again below.')
            self.message_user(request, msg, messages.SUCCESS)
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg, messages.SUCCESS)
            # use cleaner redirect to admin rather than rely on going up path
            post_url = reverse("admin:index", current_app=self.admin_site.name)
            return HttpResponseRedirect(post_url)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
         Overridden default change_view to display change form for the default singleton instance id
        """
        if object_id == str(self.singleton_instance_id):
            self.model.objects.get_or_create(pk=self.singleton_instance_id)

        if not extra_context:
            extra_context = dict()
        extra_context['skip_object_list_page'] = True

        return super(SingletonModelAdmin, self).change_view(
            request,
            object_id,
            form_url=form_url,
            extra_context=extra_context,
        )

    def history_view(self, request, object_id, extra_context=None):
        """
        Overridden default change_view to display hostory of the default singleton instance id
        """
        if not extra_context:
            extra_context = dict()
        extra_context['skip_object_list_page'] = True

        return super(SingletonModelAdmin, self).history_view(
            request,
            object_id,
            extra_context=extra_context,
        )

    """ Redundant & not needed & causes error: maximum recursion depth exceeded """
    # @property
    # def singleton_instance_id(self):
    #     return getattr(self.model, 'singleton_instance_id', self.singleton_instance_id)
