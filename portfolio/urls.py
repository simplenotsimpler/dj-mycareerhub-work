# from django.urls import path
from django_distill import distill_path
from .views import PortfolioView

# urlpatterns = [
#     path('', PortfolioView.as_view(), name='portfolio-home'),
# ]

# don't need to explicitly name index.html
# example: https://github.com/lasse-cs/django_distill_blog/blob/main/blog/urls.py
urlpatterns = [
    distill_path('', PortfolioView.as_view(),
                 name='portfolio-home'),
]
