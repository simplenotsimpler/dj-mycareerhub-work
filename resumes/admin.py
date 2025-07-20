from django.contrib import admin

from resumes.models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    #TODO tweak admin

    list_display = ['id', 'name', 'is_public', 'print_link', 'word_link']
