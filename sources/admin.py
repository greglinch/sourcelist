from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from sourcelist.settings import SITE_URL
from .models import Expertise, Person, Language, Organization, SourceForJournalist, SourceForAdmin, Page # Location,


class PageAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'page_link']
    list_display = ['title', 'page_link']
#     # list_editable = ['']
#     list_filter = ['']
    search_fields = ['title']
    readonly_fields = ['slug', 'page_link']
#     # exclude  = ['']

    def page_link(self, obj):
        if obj.slug:
            url = '{}/{}'.format(SITE_URL, obj.slug)
            link_unformatted = '<a href="{}">{}</a>'.format(url, _('View page'))
            link = format_html(link_unformatted)
        else:
            link = '-'
        return link
    page_link.short_description = _('View page')



class PersonAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {

    #     }),
    #     ('Location', {
            # 'fields': ('timezone', 'city', 'state', 'country')
    #     }),
    #     (, {}),
    # )
    fields = ['approved_by_user', 'role', 'prefix', 'pronouns', 'first_name', 'middle_name', 'last_name', 'type_of_expert', 'title', 'organization', 'website', 'expertise', 'email_address', 'phone_number_primary', 'phone_number_secondary', 'twitter', 'skype', 'language', 'timezone', 'city', 'state', 'country', 'notes', 'media_audio', 'media_text', 'media_video', 'entry_method', 'entry_type'] # 'location', 'woman', 'underrepresented', 'rating','media',
    list_display = ['last_name', 'first_name', 'updated', 'entry_method', 'entry_type', 'approved_by_user', 'role'] # 'country', 'timezone_abbrev', 'title', 'type_of_expert', 'rating' ## 'email_address', 'phone_number', 'website', 'first_last_name', 'id_as_woman', 'id_as_underrepresented',
    # list_editable = ['']
    list_filter = ['role', 'rating', 'timezone', 'city', 'state', 'country'] ## , 'title', 'underrepresented', 'woman'
    search_fields = ['city', 'country', 'email_address', 'expertise', 'first_name', 'language', 'last_name', 'notes', 'organization', 'state', 'title', 'type_of_expert', 'twitter', 'website'] # 'location', 'underrepresented', # 'expertise__name', 'language__name', 'organization__name',
    # filter_horizontal = ['expertise', 'organization', 'language']
    readonly_fields = ['rating_avg', 'role', 'rating', 'entry_method', 'entry_type']
    save_as = True
    save_on_top = True
    # exclude  = ['']

    def timezone_abbrev(self, obj):
        return obj.timezone
    timezone_abbrev.short_description = _('Timezone offset')

    ## THIS NEEDS TO SUPPORT
        # DONE if user.email is Person's email
        # ??? if person is approved (did I mean status-wise?)
    def get_queryset(self, request):
        """ only show the current user if not admin """
        qs = super(PersonAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(email_address=request.user.email)
            # return qs.filter(newsroom=request.user.documentcloudcredentials.newsroom)

    def save_model(self, request, obj, form, change):
        if not obj.created:
            ## associate the Person being created with the User who created them
            current_user = request.user
            # obj.created_by = current_user
            ## set the status
            if current_user.is_superuser == True:
                status = 'added_by_admin'
            elif current_user.email == obj.email:
                status = 'added_by_self'
            else:
                status = 'added_by_other'
            if not obj.entry_method:
                obj.entry_method = 'admin-form'
        # obj.status = status

        ## save
        super(PersonAdmin, self).save_model(request, obj, form, change)


class SourceForJournalistAdmin(admin.ModelAdmin):
    # SOURCE_FIELDS = PersonAdmin.fields
    # SOURCE_FIELDS.remove('approved_by_user')
    # fields = SOURCE_FIELDS  
    fields = PersonAdmin.fields
    # SOURCE_DISPLAY = PersonAdmin.list_display
    # SOURCE_DISPLAY.remove('approved_by_user')
    # list_display = SOURCE_DISPLAY
    list_display = PersonAdmin.list_display
    # list_editable = ['']
    list_filter = PersonAdmin.list_filter
    search_fields = PersonAdmin.search_fields
    readonly_fields = fields

    def timezone_abbrev(self, obj):
        return obj.timezone
    timezone_abbrev.short_description = _('Timezone offset')

    def get_queryset(self, request):
        """ only show Person objects with a role of source """
        qs = super(SourceForJournalistAdmin, self).get_queryset(request)
        return qs.filter(role='source', approved_by_user=True, approved_by_admin=True)


class SourceForAdminAdmin(admin.ModelAdmin):
    fields = ['approved_by_admin', 'approved_by_user', 'declined_by_admin', 'role', 'prefix', 'pronouns', 'first_name', 'middle_name', 'last_name', 'type_of_expert', 'title', 'organization', 'website', 'expertise', 'email_address', 'phone_number_primary', 'phone_number_secondary', 'twitter', 'skype', 'language', 'timezone', 'city', 'state', 'country', 'notes', 'entry_method', 'entry_type']
    list_display = ['last_name', 'first_name', 'updated', 'entry_method', 'entry_type', 'approved_by_user', 'approved_by_admin', 'declined_by_admin', 'role' ]
    list_editable = ['approved_by_admin', 'declined_by_admin']
    list_filter = ['created', 'updated', 'approved_by_user', 'approved_by_admin', 'declined_by_admin', 'entry_method', 'entry_type'] # PersonAdmin.list_filter
    readonly_fields = ['entry_method', 'entry_type']
    search_fields = PersonAdmin.search_fields
    save_on_top = True

    def timezone_abbrev(self, obj):
        return obj.timezone
    timezone_abbrev.short_description = _('Timezone offset')

    def get_queryset(self, request):
        """ only show Person objects with a role of source """
        qs = super(SourceForAdminAdmin, self).get_queryset(request)
        return qs.filter(role='source')


class ExpertiseAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['name']
    # list_editable = ['']
    # list_filter = ['']
    search_fields = ['name']
    # exclude  = ['']


class LanguageAdmin(admin.ModelAdmin):
    # fields = ['']
    list_display = ['name']
    # list_editable = ['']
    # list_filter = ['']
    search_fields = ['']
    # exclude  = ['']


# class LocationAdmin(admin.ModelAdmin):
#     fields = ['city', 'state', 'country', 'timezone']
#     list_display = ['city', 'state', 'country', 'timezone']
#     # list_editable = ['']
#     list_filter = ['state', 'country', 'timezone']
#     search_fields = ['city', 'state', 'country', 'timezone']
#     # exclude  = ['']


class OrganizationAdmin(admin.ModelAdmin):
    fields = ['name'] # 'location',
    list_display = ['name']
    # list_editable = ['']
    # list_filter = ['']
    search_fields = ['name']
    # exclude  = ['']


# class JournalistAdmin(admin.ModelAdmin):
#     fields = ['']
#     list_display = ['']
#     # list_editable = ['']
#     list_filter = ['']
#     search_fields = ['']
#     # exclude  = ['']


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
admin.site.register(Expertise, ExpertiseAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Language, LanguageAdmin)
# admin.site.register(Location, LocationAdmin)
admin.site.register(Organization, OrganizationAdmin)
# admin.site.register(Journalist, JournalistAdmin)
admin.site.register(SourceForJournalist, SourceForJournalistAdmin)
admin.site.register(SourceForAdmin, SourceForAdminAdmin)
