from django import forms
from django.utils.translation import ugettext_lazy as _
from sources.models import Person
# from sources.choices import MEDIA_CHOICES


FIELDS_PUBLIC = ['prefix', 'pronouns', 'first_name', 'middle_name', 'last_name', 'type_of_expert', 'title', 'organization', 'website', 'expertise', 'email_address', 'phone_number_primary', 'phone_number_secondary', 'skype', 'twitter', 'language', 'timezone', 'city', 'state', 'country', 'notes', 'media_audio', 'media_text', 'media_video']

MESSAGE_CHOICES = (
    (None, '------'),
    ('general', _('General contact')),
    ('volunteer', _('Volunteer to help')),
    ('share-success', _('Share your succes story')),
    ('request-update', _('Profile update request')),
    ('feature-requset', _('New feature request')),
    ('website-error', _('Website error')),
)

ROLE_CHOICES = (
    (None, '------'),
    ('source', _('Expert')),
    ('journalist', _('Journalist')),
    ('other', _('Other')),
)


class ContactForm(forms.Form):
    name = forms.CharField(required=True, label=_('Your full name'))
    email = forms.EmailField(required=True, label=_('Your email address'))
    message_type = forms.ChoiceField(
        choices=MESSAGE_CHOICES,
        required=True,
        initial='----',
        label=_('I\'m getting in touch because...')
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        required=True,
        initial='----',
        label=_('I\'m a...')
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea,
        label=_('Message')
    )


class GeneralInfoForm(forms.Form):
    # additional info
    # profile_id = forms.CharField(label=_('Profile ID'), help_text='Must be a number.')  # TODO update to integer after ID + parsing fixed
    profile_id = forms.IntegerField(
        label=_('Profile ID'),
        help_text='Read-only',
        # widget=forms.TextInput(attrs={'readonly':'readonly'}),
        widget=forms.HiddenInput()
    )
    link = forms.URLField(label=_('Link to current information'), help_text='This will help us confirm the details.', required=False)
    explanation = forms.CharField(widget=forms.Textarea, label=_('Explanation/notes'), help_text='What are the updated details?', required=False)


class ReportOutdatedForm(GeneralInfoForm, ContactForm):
    # remove these from ContactForm
    message = None
    message_type = None
    role = None
    # public fields
    prefix = forms.BooleanField(label=_('Prefix'), required=False)
    pronouns = forms.BooleanField(label=_('Pronouns'), required=False)
    first_name = forms.BooleanField(label=_('First name'), required=False)
    middle_name = forms.BooleanField(label=_('Middle name'), required=False)
    last_name = forms.BooleanField(label=_('Last name'), required=False)
    type_of_expert = forms.BooleanField(label=_('Type of expert'), required=False)
    title = forms.BooleanField(label=_('Title'), required=False)
    organization = forms.BooleanField(label=_('Organization'), required=False)
    website = forms.BooleanField(label=_('Website'), required=False)
    expertise = forms.BooleanField(label=_('Expertise'), required=False)
    email_address = forms.BooleanField(label=_('Email address'), required=False)
    phone_number_primary = forms.BooleanField(label=_('Phone number primary'), required=False)
    phone_number_secondary = forms.BooleanField(label=_('Phone number secondary'), required=False)
    skype = forms.BooleanField(label=_('Skype'), required=False)
    twitter = forms.BooleanField(label=_('Twitter'), required=False)
    language = forms.BooleanField(label=_('Language'), required=False)
    timezone = forms.BooleanField(label=_('Timezone'), required=False)
    city = forms.BooleanField(label=_('City'), required=False)
    state = forms.BooleanField(label=_('State'), required=False)
    country = forms.BooleanField(label=_('Country'), required=False)
    notes = forms.BooleanField(label=_('Notes'), required=False)
    media_audio = forms.BooleanField(label=_('Media audio'), required=False)
    media_text = forms.BooleanField(label=_('Media text'), required=False)
    media_video = forms.BooleanField(label=_('Media video'), required=False)


# class SubmitForm(forms.ModelForm):
#     # media_field = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=MEDIA_CHOICES) #, verbose_name='Which types of media are you interested interested or experienced in being a source?', help_text='Choose all that apply.')

#     class Meta:
#         model = Person
#         # fields_to_use = FIELDS_PUBLIC
#         # fields_to_use.pop(-1)
#         # fields_to_use.append('media_field')
#         fields = FIELDS_PUBLIC

class ReportUpdateForm(GeneralInfoForm, ContactForm):
    # remove these from ContactForm
    message = None
    message_type = None
    role = None

    # class Meta:
    #     contact_fields = list(ContactForm().fields.keys())
    #     general_fields = list(GeneralInfoForm().fields.keys())
    #     # import pdb; pdb.set_trace()
    #     fields = contact_fields + general_fields

    # def __init__(self, *args, **kwargs):
        # super(ReportUpdateForm, self).__init__(*args, **kwargs)
        # self.fields.pop('message')
        # self.fields.pop('message_type')
        # self.fields.pop('role')
