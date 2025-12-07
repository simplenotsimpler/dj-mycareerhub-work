import logging

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from common.github import get_projects
from core.models import Keyword
from portfolio.models import Portfolio

from .forms import ContactSubmissionForm
from django.core.mail import EmailMessage

# Set up logger
logger = logging.getLogger(__name__)


class PortfolioView(TemplateView):
    template_name = 'portfolio/portfolio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        portfolio = get_object_or_404(Portfolio, is_active=True)
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

            # Log form submission
            logger.info(
                f"Contact form submitted by {submission.name} ({submission.email})")

            # Prepare the email
            subject = f'Contact from {submission.name}'
            message = f"You received a new contact message from {submission.name} <{submission.email}>:\n\n{submission.message}"
            from_email = context['basics'].email
            recipient_list = [context['basics'].email]

            # email = EmailMessage(
            #     subject=subject,
            #     body=message,
            #     from_email=from_email,
            #     to=recipient_list,
            #     # allows developer to reply directly
            #     reply_to=[submission.email],
            # )
            # email.send(fail_silently=False)
            try:
                email = EmailMessage(
                    subject=subject,
                    body=message,
                    from_email=from_email,
                    to=recipient_list,
                    # allows developer to reply directly
                    reply_to=[submission.email],
                )
                email.send(fail_silently=False)
                logger.info(f"Email sent successfully to {recipient_list}")

                messages.success(
                    request, "Thank you! Your message has been sent.")

            except Exception as e:
                logger.error(f"Error sending email: {e}")
                messages.error(
                    request, "There was an error sending your message. Please try again later.")

            # Redirect to GET to prevent form resubmission. This resets form.
            return redirect(reverse('portfolio-home'))
        else:
            # Keep invalid form with errors
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)
