from __future__ import unicode_literals
from django.db import models
from sources.choices import PREFIX_CHOICES

class BasicInfo(models.Model):
    """ abstract base class used across models """
    created = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    systemupdated = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name="Updated in system", help_text="This is when the item was updated in the system.") 

    class Meta:
        abstract = True


class Expertise(BasicInfo):
    

    def __unicode__(self):
        return "%s" % (self.name)


class Location(BasicInfo):
    """ for Person and Organization """
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    timezone = models.CharField(max_length=255, null=True, blank=True) ## lookup based on city/state/county combo?

    def __unicode__(self):
        return "%s" % (self.name)


class Organization(BasicInfo):
    """ for Sources and Journalists """
    location = models.ForeignKey(Location, null=True)
    website = models.URLField(max_length=200)

    def __unicode__(self):
        return "%s" % (self.name)


class Person(BasicInfo):
    """ abstract base class used for Sources and Journalists """
    email_address = models.EmailField(max_length=254)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    location = models.ForeignKey(Location, null=True)
    notes = models.TextField(null=True, blank=True)
    organization = models.ForeignKey(Organization, null=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    prefix = models.CharField(PREFIX_CHOICES)
    rating = models.PositiveIntegerField(null=True, blank=True) ## or should it be choices field with 1-10?
    title = models.CharField(max_length=255, null=True, blank=True)
    underrepresented = models.BooleanField(default=No, verbose_name="Do you identify as a member of an underrepresented group?")
    website = models.CharField(max_length=255, null=True, blank=True)
    woman = models.BooleanField(default=No, verbose_name="Do you identify as a woman?")

    def __unicode__(self):
        return "%s" % (self.name)

    class Meta:
        abstract = True
        verbose_name = "People"


class Journalist(Person):
    """ people who use the Sources """

    def __unicode__(self):
        return "%s" % (self.name)

class Source(Person):
    """ sources for Journalists """
    approved = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s" % (self.name)




