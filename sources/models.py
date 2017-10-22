from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from sources.choices import PERSON_CHOICES, PREFIX_CHOICES, RATING_CHOICES, STATUS_CHOICES, COUNTRY_CHOICES


class BasicInfo(models.Model):
    """ abstract base class used across models """
    created = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name='Updated in system', help_text='This is when the item was updated in the system.')

    class Meta:
        abstract = True


class Expertise(BasicInfo):
    name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Expertise'

    def __unicode__(self):
        return '{}'.format(self.name)


class Language(BasicInfo):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return '{}'.format(self.name)


class Organization(BasicInfo):
    """ for Sources and Journalists """
    name = models.CharField(max_length=255, null=True, blank=True)
    # location = models.ForeignKey(Location, null=True, blank=True)
    # website = models.URLField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return '{}'.format(self.name)


class Person(BasicInfo):
    """ class to be inherited by Sources and Journalists """
    approved_by_user = models.BooleanField(default=False)
    approved_by_admin = models.BooleanField(default=False)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, choices=COUNTRY_CHOICES, null=True)
    email_address = models.EmailField(max_length=254)
    expertise = models.CharField(max_length=255, null=True, blank=True, help_text='Comma-separated list')
    # expertise = models.ManyToManyField(Expertise, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=False)
    last_name = models.CharField(max_length=255, null=True, blank=False)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=255, null=True, blank=True, help_text='Comma-separated list')
    # language = models.ManyToManyField(Language)
    # location = models.ForeignKey(Location, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    organization = models.CharField(max_length=255, null=True, blank=True) # , help_text='Comma-separated list')
    # organization = models.ManyToManyField(Organization, blank=True)
    phone_number_primary = models.CharField(max_length=15, null=True, blank=True, verbose_name='Primary phone number', help_text='Ideally a cell phone')
    phone_number_secondary = models.CharField(max_length=15, null=True, blank=True, verbose_name='Secondary phone number')
    prefix = models.CharField(choices=PREFIX_CHOICES, max_length=5, null=True, blank=True)
    rating = models.PositiveIntegerField(null=True, blank=True) ## switch rating to ManyToManyField?
    rating_avg = models.IntegerField(null=True, blank=True)
    role = models.CharField(choices=PERSON_CHOICES, max_length=255, null=True, blank=False, default='source')
    slug = models.CharField(null=True, blank=True, max_length=50) # .SlugField(max_length=50)
    state = models.CharField(max_length=255, null=True, blank=True, verbose_name='State/province')
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    timezone = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(-12),MaxValueValidator(12)], verbose_name='Time zone offset') ## lookup based on city/state/county combo?
    type_of_scientist = models.CharField(max_length=255, null=True, blank=True)
    # underrepresented = models.BooleanField(default=False, verbose_name='Do you identify as a member of an underrepresented group?')
    website = models.URLField(max_length=255, null=True, blank=True)
    # woman = models.BooleanField(default=False, verbose_name='Do you identify as a woman?'')
    created_by = models.ForeignKey(User, null=True, blank=True, related_name='created_by_person')
    related_user = models.ForeignKey(User, null=True, blank=True, related_name='related_user_person')

    def first_last_name(self):
        if self.middle_name:
            return '{} {}'.format(self.first_name, self.middle_name, self.last_name)
        else:
            return '{} {}'.format(self.first_name, self.last_name)
    first_last_name.short_description = 'Name'
        
    # def id_as_woman(self):
    #     return self.woman
    # id_as_woman.short_description = 'Woman?'
    # id_as_woman.boolean = True

    # def id_as_underrepresented(self):
    #     return self.underrepresented
    # id_as_underrepresented.short_description = "Underrepresented?"
    # id_as_underrepresented.boolean = True

    def save(self, *args, **kwargs):
    #     ## avg of all ratings
    #     # self.rating_avg = # Aggregate Avg of all ratings for this user
        if self.approved_by_user or self.approved_by_admin:
            self.status = 'approved'
        if not self.slug:
            self.slug = slugify(self.first_name + '-' + self.last_name)
        return super(Person, self).save(*args, **kwargs) 

    def __unicode__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    class Meta:
        verbose_name_plural = 'People'


@receiver(post_save, sender=Person, dispatch_uid='send_user_added_email')
def send_user_added_email(sender, instance, **kwargs):
    ## trigger mgmt cmd to notify user they've been created and by whom
    email_address = instance.email_address
    status = instance.status

    status = instance.status
    status_type = status.split('_')[0]
    role = instance.role

    if role == 'source': # and instance.created == instance.updated:
        if status_type == 'added':
            call_command('set_related_user', email_address)
            call_command('email_user', email_address, status)
        else:
            call_command('set_related_user', email_address)
    ## TK TK: need a way to handle journalists role for this so it will update the User model, but not send too many emails


class Rating(BasicInfo):
    """ a Journalist can rate a Source each time """
    # notes = models.TextField(null=True, blank=True, help_text='Optional')
    rating = models.CharField(choices=RATING_CHOICES, null=True, blank=True, max_length=255)
    ## these are FK to allow for multiples -- not just one
    created_by = models.ForeignKey(User, null=True, blank=True, related_name='created_by_rating')
    related_user = models.ForeignKey(User, null=True, blank=True, related_name='related_user_rating')

    def __unicode__(self):
        return '{} {} {}'.format(self.prefix, self.first_name, self.last_name)

    class Meta:
        ordering = ['updated']


# class Journalist(Person):
#     """ people who use the Sources """

#     class Meta:
#         proxy = True

#     def __unicode__(self):
#         return '{} {} {}' % (self.prefix, self.first_name, self.last_name)

class Source(Person):
    """ sources for Journalists """

    class Meta:
        proxy = True

    def __unicode__(self):
        return '{} {} {}'.format(self.prefix, self.first_name, self.last_name)




