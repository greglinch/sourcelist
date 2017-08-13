from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Expertise, Person, Language, Organization # Location,


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
    fields = ['role', 'prefix', 'first_name', 'middle_name', 'last_name', 'title', 'organization', 'website', 'expertise', 'email_address', 'phone_number_primary', 'phone_number_secondary', 'notes', 'rating', 'language', 'timezone', 'city', 'state', 'country'] # 'location', 'woman', 'underrepresented',
    list_display = ['last_name', 'first_name', 'role', 'country', 'timezone', 'title', 'rating' ] ## 'email_address', 'phone_number', 'website', 'first_last_name', 'id_as_woman', 'id_as_underrepresented',
    # list_editable = ['']
    list_filter = ['role', 'rating', 'timezone', 'city', 'state', 'country'] ## , 'title', 'underrepresented', 'woman'
    search_fields = ['city', 'country', 'email_address', 'expertise', 'first_name', 'last_name', 'notes', 'organization', 'state', 'title', 'underrepresented', 'website'] # 'location', 
    filter_horizontal = ['expertise', 'organization', 'language']
    readonly_fields = ['rating']
    # exclude  = ['']

    ## THIS ALSO NEEDS TO SUPPORT 
        # if user.email is Person's email
        # if person is approved
    # def get_queryset(self, request):
    # """ only show people added by the current user """
    #     qs = super(DocumentAdmin, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     else:
    #         return qs.filter(user=request.user)
    #         # return qs.filter(newsroom=request.user.documentcloudcredentials.newsroom)

    def save_model(self, request, obj, form, change):
        ## based on the Person being created, create a new User if they don't exist
        try:
            user_existing = User.objects.get(email=obj.email_address)
        except:
            user_existing = False
        if user_existing:
            obj.related_user = user_existing
        else:
            username = '{}{}'.format(obj.first_name, obj.last_name).lower().replace('-','')
            import random
            choices = 'abcdefghijklmnopqrstuvwxyz0123456789'
            middle_choices = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
            password = \
                ''.join([random.SystemRandom().choice(choices) for i in range(1)]) + \
                ''.join([random.SystemRandom().choice(middle_choices) for i in range(23)]) + \
                ''.join([random.SystemRandom().choice(choices) for i in range(1)])
            user_new = User.objects.create_user(username, password=password)
            user_new.email = obj.email_address
            user_new.first_name = obj.first_name
            user_new.last_name = obj.last_name
            user_new.save()
            ## trigger mgmt cmd to notify user they've been created and by whom
            # from django.core import management.call_command
            # call_command()
        # except:
        #     message = 'Error adding user.'
        #     messages.error(request, message)
        ## associate the Person being created with the User who created them
        current_user = request.user
        obj.created_by = current_user
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
admin.site.register(Expertise, ExpertiseAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Language, LanguageAdmin)
# admin.site.register(Location, LocationAdmin)
admin.site.register(Organization, OrganizationAdmin)
# admin.site.register(Journalist, JournalistAdmin)
# admin.site.register(Source, SourceAdmin)