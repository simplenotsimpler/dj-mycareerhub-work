from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from common.github import get_projects
from core.models import Keyword
from portfolio.models import Portfolio

from .forms import ContactSubmissionForm
from django.core.mail import EmailMessage


class PortfolioView(TemplateView):
    template_name = 'portfolio/portfolio.html'

    def get_object_or_404(self):
        obj = Portfolio.load()
        if not obj:
            raise Http404("Portfolio not found")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        portfolio = self.get_object_or_404()
        # context['portfolio'] = portfolio
        # context["projects"] = get_projects()
        # context['skills'] = Keyword.group_by_skill(portfolio.keywords.all())

        context.update({
            "portfolio": portfolio,
            "basics": portfolio.basics,
            "seo": portfolio.seo_config,
            "about_hero": portfolio.about_hero,
            "navigation": portfolio.navigation,
            "quote": portfolio.quote,
            "social_profiles": portfolio.social_profiles.all(),
            "projects": get_projects(),
            "skills": Keyword.group_by_skill(portfolio.keywords.all()),
            "form": ContactSubmissionForm(),
        })
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = ContactSubmissionForm(request.POST)

        if form.is_valid():
            submission = form.save()

            # Prepare the email
            subject = f'Contact from {submission.name}'
            message = f"You received a new contact message from {submission.name} <{submission.email}>:\n\n{submission.message}"
            from_email = context['basics'].email
            recipient_list = [context['basics'].email]

            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=from_email,
                to=recipient_list,
                # allows developer to reply directly
                reply_to=[submission.email],
            )
            email.send(fail_silently=False)

            messages.success(request, "Thank you! Your message has been sent.")            

            # Redirect to GET to prevent form resubmission. This resets form.
            return redirect(reverse('portfolio-home'))
        else:
            # Keep invalid form with errors
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)