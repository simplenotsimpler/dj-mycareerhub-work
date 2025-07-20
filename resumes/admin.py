from django.contrib import admin

from resumes.models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    pass
   
    # list_display = ['name', 'is_public', 'print_link', 'word_link']
