# NOTE: This is a python package so no need to add it to Django apps
from docxtpl import DocxTemplate
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from common.utils import StaffRequiredMixin
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


class ResumeContextMixin:
    def get_resume_context(self, resume):
        resume.basics.website = clean_uri(resume.basics.website)
        socials = resume.social_profiles.all()
        social_urls = [clean_uri(s.url) for s in socials]
        return {
            'basics': resume.basics,
            'social_urls': social_urls,
            'skills': Keyword.group_by_skill(resume.keywords.all()),
            'jobs': resume.jobs.all().order_by('-start_date'),
            'educations': resume.educations.all().order_by('-start_date'),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resume = self.get_object()
        context.update(self.get_resume_context(resume))
        return context


class ResumeDetailView(StaffRequiredMixin, ResumeContextMixin, DetailView):
    model = Resume
    template_name = 'resume/resume.html'


class ResumeDocxView(StaffRequiredMixin, ResumeContextMixin, DetailView):
    model = Resume

    def render_to_response(self, context, **response_kwargs):
        # ← Make sure this path is correct
        tpl = DocxTemplate("templates/resume/resume_template.docx")
        tpl.render(context)
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response['Content-Disposition'] = f'attachment; filename=resume-{self.object.pk}.docx'
        tpl.save(response)
        return response

