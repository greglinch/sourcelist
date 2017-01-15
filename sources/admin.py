from django.contrib import admin
from .models import Expertise, Journalist, Location, Organization, Source


class ExpertiseAdmin(admin.ModelAdmin):
    # fields = ['']
    list_display = 
    # list_editable = ['']
    list_filter = 
    search_fields = 
    # exclude  = ['']


class JournalistAdmin(admin.ModelAdmin):
    # fields = ['']
    list_display = 
    # list_editable = ['']
    list_filter = 
    search_fields = 
    # exclude  = ['']


class LocationAdmin(admin.ModelAdmin):
    # fields = ['']
    list_display = 
    # list_editable = ['']
    list_filter = 
    search_fields = 
    # exclude  = ['']


class OrganizationAdmin(admin.ModelAdmin):
    # fields = ['']
    list_display = 
    # list_editable = ['']
    list_filter = 
    search_fields = 
    # exclude  = ['']


class SourceAdmin(admin.ModelAdmin):
    # fields = ['']
    list_display = 
    # list_editable = ['']
    list_filter = 
    search_fields = 
    # exclude  = ['']


## TEMPLATE
# class Admin(admin.ModelAdmin):
#     fields = ['']
#     list_display = 
#     # list_editable = ['']
#     list_filter = 
#     search_fields = 
#     # exclude  = ['']

## TEMPLATE
# admin.site.register(Model, ModelAdmin)
admin.site.register(Expertise, ExpertiseAdmin)
admin.site.register(Journalist, JournalistAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Source, SourceAdmin)