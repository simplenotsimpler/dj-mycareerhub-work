from django.contrib import admin

from reports.models import ContactBackgroundCheck, ContactReferences, EducHistory, WorkHistory

# https://forum.djangoproject.com/t/creating-a-base-modeladmin-for-a-project/2944

# TODO add report date
# TODO remove current work here


class ReportsAdmin(admin.ModelAdmin):
    # NOTE: not sure if I want this removed when I'm listing things like Education History, etc.
    list_display_links = None

    def changelist_view(self, request, extra_context=None):
        # this works even though looks like IDE is not autosuggesting!!
        extra_context = {'title': self.model._meta.verbose_name}
        return super().changelist_view(request, extra_context=extra_context)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(EducHistory)
class EducHistoryAdmin(ReportsAdmin):
    list_display = ['degree_field', 'institution',
                    'location', 'start_to_end', 'gpa', 'note']


@admin.register(WorkHistory)
class WorkHistoryAdmin(ReportsAdmin):

  # TODO maybe skip present since have is current position?
    list_display = ['position', 'org', 'job_address',
                    'start_date_formatted', 'end_date_or_present', 'is_current_position', 'salary_from', 'salary_to', 'salary_per', 'employment_type', 'reason_for_leaving']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("job_highlights")


class ContactListDisplayMixin:
    list_display = ['full_name', 'phone', 'email',
                    'position', 'org', 'relationship', 'known_since', 'how_long_known']

#TODO: changelist template
@admin.register(ContactReferences)
class ContactReferencesAdmin(ContactListDisplayMixin, ReportsAdmin):
    pass

#TODO: changelist template
@admin.register(ContactBackgroundCheck)
class ContactBackgroundCheckAdmin(ContactListDisplayMixin, ReportsAdmin):
    pass
