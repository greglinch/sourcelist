from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from sources.choices import PERSON_CHOICES, PREFIX_CHOICES, RATING_CHOICES, STATUS_CHOICES, COUNTRY_CHOICES, ENTRY_CHOICES#, MEDIA_CHOICES


class BasicInfo(models.Model):
    """ abstract base class used across models """
    created = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name=_('Updated in system'), help_text=_('This is when the item was updated in the system.'))

    class Meta:
        abstract = True


class Expertise(BasicInfo):
    name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = _('Expertise')

    def __str__(self):
        return '{}'.format(self.name)


class Language(BasicInfo):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.name)


class Organization(BasicInfo):
    """ for Sources and Journalists """
    name = models.CharField(max_length=255, null=True, blank=True)
    # location = models.ForeignKey(Location, null=True, blank=True)
    # website = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.name)


class Page(BasicInfo):
    content = models.TextField(null=True, blank=True)
    # description = models.CharField(blank=True, null=True, max_length=160, help_text=_('Limit: 160 characters'))
    # header = models.TextField(blank=True, null=True, help_text=_('Items to add to the header (e.g. metadata, CSS, JS, etc)'))
    title = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Page, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.title)


class Person(BasicInfo):
    """ class to be inherited by Sources and Journalists """
    # added_by_other = models.BooleanField(default=False, verbose_name=_('Is the person you just added not you?'))
    approved_by_user = models.BooleanField(default=False)
    approved_by_admin = models.BooleanField(default=False)
    city = models.CharField(max_length=255, null=True, blank=False, verbose_name=_('City'))
    country = models.CharField(max_length=255, choices=COUNTRY_CHOICES, null=True, blank=False, verbose_name=_('Country'))
    declined_by_admin = models.BooleanField(default=False, verbose_name=_('Declined'))
    email_address = models.EmailField(max_length=254, null=True, blank=False, verbose_name=_('Email address'))
    entry_method = models.CharField(max_length=15, null=True, blank=True)
    entry_type = models.CharField(max_length=15, null=True, blank=True, default='manual')
    expertise = models.CharField(max_length=255, null=True, blank=True, help_text=_('Comma-separated list'), verbose_name=_('Expertise'))
    # expertise = models.ManyToManyField(Expertise, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=False, verbose_name=_('First name'))
    last_name = models.CharField(max_length=255, null=True, blank=False, verbose_name=_('Last name'))
    media_audio = models.BooleanField(default=False, verbose_name=_('Audio/radio/podcast'))
    media_text = models.BooleanField(default=False, verbose_name=_('Text/print'))
    media_video = models.BooleanField(default=False, verbose_name=_('Video/TV'))
    middle_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Middle name'))
    language = models.CharField(max_length=255, null=True, blank=True, help_text=_('Comma-separated list'), verbose_name=_('Language'))
    # language = models.ManyToManyField(Language)
    # location = models.ForeignKey(Location, null=True, blank=True)
    notes = models.TextField(null=True, blank=True, verbose_name=_('Public notes'), help_text=_('If you would like to share the underrepresented group(s) you identify with, please do so here.'))
    organization = models.CharField(max_length=255, null=True, blank=False, verbose_name=_('Organization')) # , help_text=_('Comma-separated list'))
    # organization = models.ManyToManyField(Organization, blank=True)
    phone_number_primary = models.CharField(max_length=30, null=True, blank=False, verbose_name=_('Primary phone number'), help_text=_('Ideally a cell phone'))
    phone_number_secondary = models.CharField(max_length=30, null=True, blank=True, verbose_name=_('Secondary phone number'))
    prefix = models.CharField(choices=PREFIX_CHOICES, max_length=5, null=True, blank=True, verbose_name=_('Prefix'))
    pronouns = models.CharField(null=True, blank=True, max_length=255, help_text=_('e.g. she/her, they/their, etc.'), verbose_name=_('Pronouns')) ## switch to ManyToManyField? # help_text=_('Everyone is encouraged to enter theirs so journalists know which ones to use (e.g. she/her, they/their, etc.))
    rating = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Rating')) ## switch rating to ManyToManyField?
    rating_avg = models.IntegerField(null=True, blank=True, verbose_name=_('Rating average'))
    role = models.CharField(choices=PERSON_CHOICES, max_length=255, null=True, blank=False, default='source', verbose_name=_('Role'))
    skype = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Skype username'))
    slug = models.CharField(null=True, blank=True, max_length=50) # .SlugField(max_length=50)
    state = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('State/province'))
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Title'))
    timezone = models.IntegerField(null=True, blank=False, validators=[MinValueValidator(-12),MaxValueValidator(12)], verbose_name=_('Time zone offset from GMT'), help_text=_('-4, 10, etc.')) ## lookup based on city/state/county combo?
    twitter = models.CharField(null=True, blank=True, max_length=140, help_text=_('Please do not include the @ symbol'), verbose_name=_('Twitter'))
    type_of_expert = models.CharField(max_length=255, null=True, blank=False, help_text=_('e.g. Biologist, Engineer, Mathematician, Sociologist, etc.'), verbose_name=_('Type of expert'))
    # underrepresented = models.BooleanField(default=False, verbose_name=_('Do you identify as a member of an underrepresented group?'))
    website = models.URLField(max_length=255, null=True, blank=False, help_text=_("Please include http:// at the beginning."), verbose_name=_('Website'))
    # woman = models.BooleanField(default=False, verbose_name=_('Do you identify as a woman?''))
    # created_by = models.ForeignKey(User, null=True, blank=True, related_name='created_by_person', on_delete=models.SET_NULL)
    related_user = models.ForeignKey(User, null=True, blank=True, related_name='related_user_person', on_delete=models.SET_NULL)

    def first_last_name(self):
        if self.middle_name:
            return '{} {}'.format(self.first_name, self.middle_name, self.last_name)
        else:
            return '{} {}'.format(self.first_name, self.last_name)
    first_last_name.short_description = _('Name')
        
    # def id_as_woman(self):
    #     return self.woman
    # id_as_woman.short_description = _('Woman?')
    # id_as_woman.boolean = True

    # def id_as_underrepresented(self):
    #     return self.underrepresented
    # id_as_underrepresented.short_description = _('Underrepresented?')
    # id_as_underrepresented.boolean = True

    # def get_field_values(self):
    #     return [field.value_to_string(self) for field in Person._meta.fields]

    # def get_person_dict(self):
    #     person_dict = {}
    #     fields = Person._meta.fields
    #     for field in fields:
    #         field_name = field.name
    #         field_value = field.value_to_string(self)
    #         person_dict[field_name] = field_value
    #     return person_dict

    def get_absolute_url(self):
        """ preferred/abstract way to defin the URL """
        return reverse('source', args=[self.slug])

    def save(self, *args, **kwargs):
    #     ## avg of all ratings
    #     # self.rating_avg = # Aggregate Avg of all ratings for this user
        if self.approved_by_user or self.approved_by_admin:
            self.status = 'approved'
        elif not self.status:
            self.status = 'added'
        # if self.added_by_other:
        #     self.status = 'added_by_other'
        if not self.slug:
            first = self.first_name #.replace(r'^".*"$', '')
            last = self.last_name
            self.slug = slugify(first + '-' + last)
        if self.twitter:
            self.twitter = self.twitter.replace('@', '')
        if not self.entry_method:
            self.entry_method = 'site-form'
        return super(Person, self).save(*args, **kwargs) 

    def __str__(self):
        if self.prefix and self.middle_name:
            name = '{} {} {} {}'.format(self.prefix, self.first_name, self.middle_name, self.last_name)
        elif self.prefix:
            name = '{} {} {}'.format(self.prefix, self.first_name, self.last_name)
        elif self.middle_name:
            name = '{} {} {}'.format(self.first_name, self.middle_name, self.last_name)
        else:
            name = '{} {}'.format(self.first_name, self.last_name)
        return name

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('People')


@receiver(post_save, sender=Person, dispatch_uid='build_watson_search_index')
def build_watson_search_index(sender, instance, **kwargs):
    call_command('buildwatson')

# @receiver(post_save, sender=Person, dispatch_uid='send_user_added_email')
# def send_user_added_email(sender, instance, **kwargs):
#     ## trigger mgmt cmd to notify user they've been created and by whom
#     email_address = instance.email_address
#     status = instance.status

#     status = instance.status
#     status_type = status.split('_')[0]
#     role = instance.role

#     if role == 'source': # and instance.created == instance.updated:
#         if status_type == 'added':
#             call_command('set_related_user', email_address)
#             if instance.entry_type == 'manual':
#                 call_command('email_user', email_address, status)
#         else:
#             call_command('set_related_user', email_address)
    ## TK TK: need a way to handle journalists role for this so it will update the User model, but not send too many emails


class Rating(BasicInfo):
    """ a Journalist can rate a Source each time """
    # notes = models.TextField(null=True, blank=True, help_text=_('Optional'))
    rating = models.CharField(choices=RATING_CHOICES, null=True, blank=True, max_length=255)
    ## these are FK to allow for multiples -- not just one
    created_by = models.ForeignKey(User, null=True, blank=True, related_name='created_by_rating', on_delete=models.SET_NULL)
    related_user = models.ForeignKey(User, null=True, blank=True, related_name='related_user_rating', on_delete=models.SET_NULL)

    def __str__(self):
        return '{} {} {}'.format(self.prefix, self.first_name, self.last_name)

    class Meta:
        verbose_name = _('Rating')
        verbose_name_plural = _('Ratings')
        ordering = ['updated']


# class Journalist(Person):
#     """ people who use the Sources """

#     class Meta:
#         proxy = True

#     def __str__(self):
#         return '{} {} {}' % (self.prefix, self.first_name, self.last_name)


class SourceForAdmin(Person):
    """ sources for admin """

    class Meta:
        proxy = True
        verbose_name = _('Source for admins')
        verbose_name_plural = _('Sources for admins')
        ordering = ['-updated']

    def __str__(self):
        if self.prefix and self.middle_name:
            name = '{} {} {} {}'.format(self.prefix, self.first_name, self.middle_name, self.last_name)
        elif self.prefix:
            name = '{} {} {}'.format(self.prefix, self.first_name, self.last_name)
        elif self.middle_name:
            name = '{} {} {}'.format(self.first_name, self.middle_name, self.last_name)
        else:
            name = '{} {}'.format(self.first_name, self.last_name)
        return name


class SourceForJournalist(Person):
    """ sources for Journalists """

    class Meta:
        proxy = True
        verbose_name = _('Source for journalists')
        verbose_name_plural = _('Sources for journalists')

    def __str__(self):
        if self.prefix and self.middle_name:
            name = '{} {} {} {}'.format(self.prefix, self.first_name, self.middle_name, self.last_name)
        elif self.prefix:
            name = '{} {} {}'.format(self.prefix, self.first_name, self.last_name)
        elif self.middle_name:
            name = '{} {} {}'.format(self.first_name, self.middle_name, self.last_name)
        else:
            name = '{} {}'.format(self.first_name, self.last_name)
        return name
