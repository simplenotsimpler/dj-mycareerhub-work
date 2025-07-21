from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from core.models import Keyword
from resumes.models import Resume

'''
  NOTE: views originally developed in the dj-mch-test-resume repo
'''

from urllib.parse import urlparse


def clean_uri(string_uri):
    url = urlparse(string_uri)
    host_name = url.hostname.replace('www.', '')
    path_name = url.path

    return host_name + path_name


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Restrict access to logged-in staff users only."""

    def test_func(self):
        return self.request.user.is_staff


class ResumeDetailView(StaffRequiredMixin, DetailView):
    model = Resume

    # explicitly set the <app name>/template
    # Django does not consistently recognize otherwise
    template_name = 'resume/resume.html'

    #TODO can I reuse this for the Word view? maybe as a mixin?
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resume = self.get_object()

        # clean urls before passing to context
        resume.basics.website = clean_uri(resume.basics.website)

        socials = resume.social_profiles.all()
        socials_urls = []

        for social in socials:
            socials_urls.append(clean_uri(social.url))

        context['basics'] = resume.basics
        context['social_urls'] = socials_urls
        context['skills'] = Keyword.group_by_skill(
            resume.keywords.all())
        context['jobs'] = resume.jobs.all().order_by('-start_date')
        context['educations'] = resume.educations.all().order_by('-start_date')
        return context

#TODO: generate Word version
@staff_member_required
def get_word(request, pk):
    request_pk = pk
    print(f'primary key is: {request_pk}')
    return HttpResponse(f'primary key is: {request_pk}')
