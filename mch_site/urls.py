from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from decouple import config
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# NOTE: if see repeated attempts to /admin, install django-admin-honeypot for better tracking

urlpatterns = [
    # path('admin/', admin.site.urls),
    # hide admin url per https://www.digitalocean.com/community/tutorials/how-to-harden-your-production-django-project
    path(config('ADMIN_URL'), admin.site.urls),
    path('', include('portfolio.urls')),
    path('resumes/', include('resumes.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    # so static files work when test gunicorn locally
    # https://stackoverflow.com/questions/12800862/how-to-make-django-serve-static-files-with-gunicorn
    urlpatterns += staticfiles_urlpatterns()

admin.site.site_header = "MyCareerHub Admin Portal"
admin.site.site_title = "MyCareerHub Admin Portal"
admin.site.index_title = "Site Administration"
