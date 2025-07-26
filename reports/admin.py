from django.contrib import admin

from common.utils import ReadOnlyAdminMixin
from reports.models import ContactList, EducHistory, WorkHistory

# https://forum.djangoproject.com/t/creating-a-base-modeladmin-for-a-project/2944


class ReportsAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    # NOTE: not sure if I want this removed when I'm listing things like Education History, etc.
    list_display_links = None

    def changelist_view(self, request, extra_context=None):
        # this works even though looks like IDE is not autosuggesting!!
        extra_context = {'title': self.model._meta.verbose_name}
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(EducHistory)
class EducHistoryAdmin(ReportsAdmin):
    list_display = ['degree_field', 'institution',
                    'location', 'start_date_formatted', 'end_date_formatted', 'gpa', 'note']


@admin.register(WorkHistory)
class WorkHistoryAdmin(ReportsAdmin):
    list_display = ['position', 'org', 'job_address',
                     'start_date_formatted', 'end_date_formatted', 'salary_from', 'salary_to', 'salary_per', 'employment_type', 'reason_for_leaving', 'okay_to_contact']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("highlights")


@admin.register(ContactList)
class ContactListAdmin(ReportsAdmin):
    list_display = [
        'full_name', 'current_reference', 'background_check', 'phone',
        'email', 'position', 'org', 'relationship', 'known_since', 'how_long_known'
    ]
