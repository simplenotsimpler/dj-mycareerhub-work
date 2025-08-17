from django.contrib import admin

from common.utils import register_current_app_models

from common.utils import register_current_app_models

from common.singleton import SingletonModelAdmin
from common.utils import register_current_app_models
from portfolio.forms import NavItemAdminForm
from portfolio.models import AboutHero, NavItem, Navigation, Portfolio, Quote, SEOConfig


@admin.register(SEOConfig)
class SEOConfigAdmin(SingletonModelAdmin):
    pass


@admin.register(AboutHero)
class AboutHeroAdmin(SingletonModelAdmin):
    pass


@admin.register(Quote)
class QuoteAdmin(SingletonModelAdmin):
    pass


@admin.register(NavItem)
class NavItemAdmin(admin.ModelAdmin):
    form = NavItemAdminForm
    list_display = ['navigation', 'title', 'slug', 'order',]
    list_display_links = ['title',]
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['navigation', 'order',]


class NavItemInline(admin.TabularInline):
    model = NavItem
    extra = 0
    fields = ('title', 'slug', 'order')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order',)


@admin.register(Navigation)
class NavigationAdmin(SingletonModelAdmin):
    inlines = [NavItemInline]


@admin.register(Portfolio)
class PortfolioAdmin(SingletonModelAdmin):
    filter_horizontal = ('social_profiles', 'keywords',)


# Call the function after registering any specific model admin class.
register_current_app_models()
