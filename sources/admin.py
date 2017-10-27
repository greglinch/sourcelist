from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Expertise, Person, Language, Organization, SourceForJournalist, SourceForAdmin # Location,


class ExpertiseAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['name']
    # list_editable = ['']
    # list_filter = 
    search_fields = ['name']
    # exclude  = ['']


class PersonAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {

    #     }),
    #     ('Location', {
            # 'fields': ('timezone', 'city', 'state', 'country')
    #     }),
    #     (, {}),
    # )
    fields = ['approved_by_admin', 'approved_by_user', 'role', 'prefix', 'first_name', 'middle_name', 'last_name', 'type_of_expert', 'title', 'organization', 'website', 'expertise', 'email_address', 'phone_number_primary', 'phone_number_secondary', 'language', 'timezone', 'city', 'state', 'country', 'notes'] # 'location', 'woman', 'underrepresented', 'rating',
    list_display = ['last_name', 'first_name', 'role', 'country', 'timezone', 'title', 'type_of_expert', 'rating' ] ## 'email_address', 'phone_number', 'website', 'first_last_name', 'id_as_woman', 'id_as_underrepresented',
    # list_editable = ['']
    list_filter = ['role', 'rating', 'timezone', 'city', 'state', 'country'] ## , 'title', 'underrepresented', 'woman'
    search_fields = ['city', 'country', 'email_address', 'expertise', 'first_name', 'language', 'last_name', 'notes', 'organization', 'state', 'title', 'type_of_expert', 'twitter', 'website'] # 'location', 'underrepresented', # 'expertise__name', 'language__name', 'organization__name',
    # filter_horizontal = ['expertise', 'organization', 'language']
    readonly_fields = ['rating_avg', 'role', 'rating', 'approved_by_admin']
    save_as = True
    save_on_top = True
    # exclude  = ['']

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
            obj.created_by = current_user
            ## set the status
            if current_user.is_superuser == True:
                status = 'added_by_admin'
            elif current_user.email == obj.email:
                status = 'added_by_self'
            else:
                status = 'added_by_other'
        # obj.status = status

        ## save
        super(PersonAdmin, self).save_model(request, obj, form, change)


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
    # fields = ['']
    # list_display = 
    # list_editable = ['']
    # list_filter = 
    # search_fields = 
    # exclude  = ['']


class SourceForJournalistAdmin(admin.ModelAdmin):
    fields = ['role', 'prefix', 'first_name', 'middle_name', 'last_name', 'title', 'organization', 'website', 'expertise', 'email_address', 'phone_number_primary', 'phone_number_secondary', 'notes', 'rating_avg', 'language', 'timezone', 'city', 'state', 'country'] # 'location', 'woman', 'underrepresented',
    list_display = ['last_name', 'first_name', 'country', 'timezone', 'title', 'rating' ] ## 'email_address', 'phone_number', 'website', 'first_last_name', 'id_as_woman', 'id_as_underrepresented',
    # list_editable = ['']
    list_filter = ['rating', 'timezone', 'city', 'state', 'country'] ## , 'title', 'underrepresented', 'woman'
    search_fields = ['city', 'country', 'email_address', 'expertise', 'first_name', 'last_name', 'notes', 'organization', 'state', 'title', 'website'] # 'location',
    # filter_horizontal = ['expertise', 'organization', 'language']
    readonly_fields = fields

    def get_queryset(self, request):
        """ only show Person objects with a role of source """
        qs = super(SourceForJournalistAdmin, self).get_queryset(request)
        return qs.filter(role='source')


class SourceForAdminAdmin(admin.ModelAdmin):
    fields = ['approved_by_admin', 'approved_by_user', 'role', 'prefix', 'first_name', 'middle_name', 'last_name', 'title', 'organization', 'website', 'expertise', 'email_address', 'phone_number_primary', 'phone_number_secondary', 'notes', 'rating_avg', 'language', 'timezone', 'city', 'state', 'country'] # 'location', 'woman', 'underrepresented',
    list_display = ['last_name', 'first_name', 'country', 'timezone', 'title', 'rating' ] ## 'email_address', 'phone_number', 'website', 'first_last_name', 'id_as_woman', 'id_as_underrepresented',
    # list_editable = [''] 
    list_filter = ['rating', 'timezone', 'city', 'state', 'country'] ## , 'title', 'underrepresented', 'woman'
    search_fields = ['city', 'country', 'email_address', 'expertise', 'first_name', 'last_name', 'notes', 'organization', 'state', 'title', 'website'] # 'location',
    # filter_horizontal = ['expertise', 'organization', 'language']
    save_on_top = True

    def get_queryset(self, request):
        """ only show Person objects with a role of source """
        qs = super(SourceForAdminAdmin, self).get_queryset(request)
        return qs.filter(role='source')


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
admin.site.register(Person, PersonAdmin)
admin.site.register(Language, LanguageAdmin)
# admin.site.register(Location, LocationAdmin)
admin.site.register(Organization, OrganizationAdmin)
# admin.site.register(Journalist, JournalistAdmin)
admin.site.register(SourceForJournalist, SourceForJournalistAdmin)
admin.site.register(SourceForAdmin, SourceForAdminAdmin)
