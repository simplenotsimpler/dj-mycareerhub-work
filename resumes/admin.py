from django.contrib import admin

from resumes.models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    # TODO use the list mixin and add links
    # need to see last updated
    # TODO make it a button?
    list_display = ['id', 'name', 'is_public', 'print_link', 'word_link']
    filter_horizontal = ('social_profiles', 'keywords', 'jobs', 'educations',)
