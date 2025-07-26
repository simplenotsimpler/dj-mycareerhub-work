from django.contrib import admin

from resumes.models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):

    list_display = ['name', 'is_public', 'created_at',
                    'updated_at', 'print_link', 'word_link']
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('social_profiles', 'keywords', 'jobs', 'educations',)
