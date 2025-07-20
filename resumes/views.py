from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from core.models import Keyword
from resumes.models import Resume

'''
  NOTE: views originally developed in the dj-mch-test-resume repo
'''


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Restrict access to logged-in staff users only."""

    def test_func(self):
        return self.request.user.is_staff


class ResumeDetailView(StaffRequiredMixin, DetailView):
    # wonder if leaving out DetailView was causing the issue with template not being recognized?
    model = Resume
    # context_object_name = 'resume'
    # explicitly set the <app name>/template
    # Django does not consistently recognize otherwise
    template_name = 'resume/resume.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resume = self.get_object()

        context['basics'] = resume.basics
        # TODO need to pass formatted social urls to template
        context['socials'] = resume.social_profiles.all()
        context['skills'] = Keyword.group_by_skill(
            resume.keywords.all())
        context['jobs'] = resume.jobs.all()
        context['educations'] = resume.educations.all()
        # print(context)
        return context


@staff_member_required
def get_word(request, pk):
    request_pk = pk
    print(f'primary key is: {request_pk}')
    return HttpResponse(f'primary key is: {request_pk}')
