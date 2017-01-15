from django.contrib import admin
from .models import Topic, Person, Location, Organization


class TopicAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['name']
    # list_editable = ['']
    # list_filter = 
    search_fields = ['name']
    # exclude  = ['']


class PersonAdmin(admin.ModelAdmin):
    fields = ['role', 'prefix', 'first_name', 'last_name', 'title', 'organization', 'website', 'topic', 'location', 'email_address', 'phone_number', 'woman', 'underrepresented', 'notes', 'rating'] 
    list_display = ['last_name', 'first_name', 'role', 'country', 'timezone', 'title', 'id_as_woman', 'id_as_underrepresented', 'rating' ] ## 'email_address', 'phone_number', 'website', 'first_last_name', 
    # list_editable = ['']
    list_filter = ['role', 'underrepresented', 'woman', 'timezone', 'city', 'state', 'country', 'rating'] ## , 'title'
    search_fields = ['email_address', 'topic', 'first_name', 'last_name', 'location', 'notes', 'organization', 'title', 'underrepresented', 'website']
    filter_horizontal = ['topic', 'organization']
    readonly_fields = ['rating']
    # exclude  = ['']


class LocationAdmin(admin.ModelAdmin):
    fields = ['city', 'state', 'country', 'timezone']
    list_display = ['city', 'state', 'country', 'timezone']
    # list_editable = ['']
    list_filter = ['state', 'country', 'timezone']
    search_fields = ['city', 'state', 'country', 'timezone']
    # exclude  = ['']


class OrganizationAdmin(admin.ModelAdmin):
    fields = ['name', 'location', 'website']
    list_display = ['name', 'website']
    # list_editable = ['']
    # list_filter = ['']
    search_fields = ['name', 'website']
    # exclude  = ['']


# class JournalistAdmin(admin.ModelAdmin):
    # fields = ['']
    # list_display = 
    # list_editable = ['']
    # list_filter = 
    # search_fields = 
    # exclude  = ['']


# class SourceAdmin(admin.ModelAdmin):
    # fields = ['']
    # list_display = 
    # list_editable = ['']
    # list_filter = 
    # search_fields = 
    # exclude  = ['']


## TEMPLATE
# class Admin(admin.ModelAdmin):
#     fields = ['']
#     list_display = ['']
#     # list_editable = ['']
#     list_filter = ['']
#     search_fields = ['']
#     # exclude  = ['']

## TEMPLATE
# admin.site.register(Model, ModelAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Organization, OrganizationAdmin)
# admin.site.register(Journalist, JournalistAdmin)
# admin.site.register(Source, SourceAdmin)