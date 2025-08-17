from django.http import Http404
from django.views.generic import TemplateView

from common.github import get_projects
from core.models import Keyword
from portfolio.models import Portfolio

# TODO: style templates - not sure if want Bootstrap, my current CSS or some combo


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
        })
        return context
