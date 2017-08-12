from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from sources.choices import PERSON_CHOICES, PREFIX_CHOICES, RATING_CHOICES


class BasicInfo(models.Model):
    """ abstract base class used across models """
    created = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name="Updated in system", help_text="This is when the item was updated in the system.")

    class Meta:
        abstract = True


class Topic(BasicInfo):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return "%s" % (self.name)


class Location(BasicInfo):
    """ for Person and Organization """
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    timezone = models.CharField(max_length=255, null=True, blank=True, verbose_name="Time zone") ## lookup based on city/state/county combo?

    def __unicode__(self):
        return "%s, %s, %s" % (self.city, self.state, self.country)


class Organization(BasicInfo):
    """ for Sources and Journalists """
    name = models.CharField(max_length=255, null=True, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return "%s" % (self.name)


class Person(BasicInfo):
    """ class to be inherited by Sources and Journalists """
    approved = models.BooleanField(default=False)
    email_address = models.EmailField(max_length=254)
    first_name = models.CharField(max_length=255, null=True, blank=False)
    last_name = models.CharField(max_length=255, null=True, blank=False)
    location = models.ForeignKey(Location, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    organization = models.ManyToManyField(Organization, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    prefix = models.CharField(choices=PREFIX_CHOICES, max_length=5, null=True, blank=True)
    rating = models.PositiveIntegerField(null=True, blank=True) ## or should it be choices field with 1-10?
    title = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(choices=PERSON_CHOICES, max_length=255, null=True, blank=False)
    topic = models.ManyToManyField(Topic, blank=True)
    underrepresented = models.BooleanField(default=False, verbose_name="Do you identify as a member of an underrepresented group?")
    website = models.CharField(max_length=255, null=True, blank=True)
    woman = models.BooleanField(default=False, verbose_name="Do you identify as a woman?")
    ## updated from Location fk
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    timezone = models.CharField(max_length=255, null=True, blank=True, verbose_name="Time zone") ## lookup based on city/state/county combo?

    def first_last_name(self):
        return '%s %s' % (self.first_name, self.last_name)
    first_last_name.short_description = "Name"
        
    def id_as_woman(self):
        return self.woman
    id_as_woman.short_description = "Woman?"
    id_as_woman.boolean = True

    def id_as_underrepresented(self):
        return self.underrepresented
    id_as_underrepresented.short_description = "Underrepresented?"
    id_as_underrepresented.boolean = True

    def save(self, *args, **kwargs):
        self.city = self.location.city
        self.state = self.location.state
        self.country = self.location.country
        self.timezone = self.location.timezone

        return super(Person, self).save(*args, **kwargs) 

    def __unicode__(self):
        return "%s %s %s" % (self.prefix, self.first_name, self.last_name)

    class Meta:
        verbose_name_plural = "People"


class Rating(BasicInfo):
    """ a Journalist can rate a Source each time """
    rating = models.TextField(choices=RATING_CHOICES, null=True, blank=True, max_length=255)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return "%s %s %s" % (self.prefix, self.first_name, self.last_name)

    class Meta:
        ordering = ['updated']


# class Journalist(Person):
#     """ people who use the Sources """


#     def __unicode__(self):
#         return "%s %s %s" % (self.prefix, self.first_name, self.last_name)

# class Source(Person):
#     """ sources for Journalists """


#     def __unicode__(self):
#         return "%s %s %s" % (self.prefix, self.first_name, self.last_name)




