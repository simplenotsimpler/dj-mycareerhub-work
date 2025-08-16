from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from common.singleton import SingletonModel
from core.models import Basics, Keyword, SocialProfile


class TwitterCardType(models.Model):
    # https://developer.x.com/en/docs/x-for-websites/cards/overview/abouts-cards
    type = models.CharField(max_length=25)

    class Meta:
        verbose_name = "Twitter Card Type"
        verbose_name_plural = "Twitter Card Types"

    def __str__(self):
        return self.type


class SEOConfig(SingletonModel):
    # NOTE: do not use meta keyword tag per https://www.seo.com/basics/glossary/meta-keywords/
    # NOTE: this is in addition to info get from Basics
    title = models.CharField(max_length=50, help_text="Title/Site Name")
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='seo/', blank=True)
    og_type = models.CharField(
        max_length=120, help_text="See object types in https://ogp.me/", default='website')
    og_imgurl = models.URLField(blank=True, null=True)
    twitter_card_type = models.ForeignKey(
        TwitterCardType, on_delete=models.SET_NULL, blank=True, null=True,)

    class Meta:
        verbose_name = "SEO Config"
        verbose_name_plural = "SEO Config"

    def __str__(self):
        return f'SEO: {self.title}'


class Quote(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=125)
    cite_href = models.URLField(max_length=255, blank=True, null=True)
    cite_name = models.CharField(max_length=125, blank=True, null=True)
    quote_image = models.ImageField(upload_to='quote/', null=True, blank=True)
    quote_image_alt_text = models.CharField(
        max_length=20, null=True, blank=True)

    def __str__(self):
        return f'"{self.text}" — {self.author}'


class Navigation(SingletonModel):
    title = models.CharField(max_length=50, default='Main Navigation')

    class Meta:
        verbose_name = "Navigation Menu"
        verbose_name_plural = "Navigation Menu"

    def __str__(self):
        return self.title


class NavItem(models.Model):
    navigation = models.ForeignKey(
        Navigation,
        on_delete=models.SET_NULL, blank=True, null=True,
        related_name='nav_items',
    )
    title = models.CharField(max_length=15, unique=True)
    # use slug not url b/c using anchor tag navigation
    slug = models.SlugField(max_length=10, unique=True, help_text='Auto-filled from title only on creation; editable afterward but not auto-updated.'
                            )

    """
      PositiveIntegerField does not accept attributes in form
      See https://forum.djangoproject.com/t/when-i-define-a-range-control-widget-min-value-isnt-being-utilized/17276/14
      Use NumberField with validators instead
    """
    order = models.IntegerField(
        default=1,
        unique=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta:
        ordering = ['order']
        verbose_name = "Nav Item"
        verbose_name_plural = "Nav Items"

    def __str__(self):
        return self.title


class AboutHero(SingletonModel):
    # https://prismic.io/blog/website-hero-section
    headline = models.CharField(
        max_length=50, help_text="Can be an animated typing introduction.")
    short_description = models.TextField(max_length=200, null=True, blank=True)
    cta_text = models.CharField(max_length=25, null=True, blank=True)
    cta_nav_item = models.ForeignKey(
        NavItem, on_delete=models.SET_NULL, blank=True, null=True, related_name='about_hero')
    visual = models.ImageField(upload_to='hero/', null=True, blank=True)
    visual_alt_text = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = "About Hero"
        verbose_name_plural = "About Hero"

    class Meta:
        verbose_name = "About Hero"
        verbose_name_plural = "About Hero"

    class Meta:
        verbose_name = "About Hero"
        verbose_name_plural = "About Hero"

    def __str__(self):
        return self.headline


class Portfolio(SingletonModel):
    navigation = models.OneToOneField(
        Navigation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='portfolio'
    )
    seo_config = models.OneToOneField(
        SEOConfig, on_delete=models.SET_NULL, null=True,  related_name='portfolio', )
    #basics is just in case want to add public display name or something
    basics = models.OneToOneField(
        Basics, on_delete=models.SET_NULL, null=True, related_name='portfolio', )
    about_hero = models.OneToOneField(
        AboutHero, on_delete=models.SET_NULL, null=True, related_name='portfolio', )
    quote = models.ForeignKey(
        Quote, on_delete=models.SET_NULL, blank=True, null=True, related_name='portfolio')
    social_profiles = models.ManyToManyField(
        SocialProfile,
        blank=True,
        related_name='portfolio'
    )
    # skills pulled in via keywords
    keywords = models.ManyToManyField(
        Keyword,
        blank=True,
        related_name='portfolio'
    )

    class Meta:
        verbose_name = "Portfolio"
        verbose_name_plural = "Portfolio"

    def __str__(self):
        return f"Portfolio {self.pk or 'New'}"


# TODO ContactUs/ContactMe
# https://www.twilio.com/en-us/blog/developers/community/build-contact-form-python-django-twilio-sendgrid
# possible also reCaptcha
