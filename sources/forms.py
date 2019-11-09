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
    name = forms.CharField(required=True, label=_('Full name'))
    email = forms.EmailField(required=True, label=_('Email address'))
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

class ReportOutdatedForm(ContactForm):
    # additional info
    # profile_id = forms.CharField(label=_('Profile ID'), help_text='Must be a number.')  # TODO update to integer after ID + parsing fixed
    profile_id = forms.CharField(
        label=_('Profile ID'),
        help_text='Read-only',
        # widget=forms.TextInput(attrs={'readonly':'readonly'}),
        widget=forms.HiddenInput()
    )
    link = forms.URLField(label=_('Link to source'), help_text='This will help us verify the details.')
    notes = forms.CharField(widget=forms.Textarea, label=_('Notes'), help_text='Any additional information you would like to share.')
    # public fields
    prefix = forms.BooleanField(label=_('prefix'))
    pronouns = forms.BooleanField(label=_('pronouns'))
    first_name = forms.BooleanField(label=_('first_name'))
    middle_name = forms.BooleanField(label=_('middle_name'))
    last_name = forms.BooleanField(label=_('last_name'))
    type_of_expert = forms.BooleanField(label=_('type_of_expert'))
    title = forms.BooleanField(label=_('title'))
    organization = forms.BooleanField(label=_('organization'))
    website = forms.BooleanField(label=_('website'))
    expertise = forms.BooleanField(label=_('expertise'))
    email_address = forms.BooleanField(label=_('email_address'))
    phone_number_primary = forms.BooleanField(label=_('phone_number_primary'))
    phone_number_secondary = forms.BooleanField(label=_('phone_number_secondary'))
    skype = forms.BooleanField(label=_('skype'))
    twitter = forms.BooleanField(label=_('twitter'))
    language = forms.BooleanField(label=_('language'))
    timezone = forms.BooleanField(label=_('timezone'))
    city = forms.BooleanField(label=_('city'))
    state = forms.BooleanField(label=_('state'))
    country = forms.BooleanField(label=_('country'))
    notes = forms.BooleanField(label=_('notes'))
    media_audio = forms.BooleanField(label=_('media_audio'))
    media_text = forms.BooleanField(label=_('media_text'))
    media_video = forms.BooleanField(label=_('media_video'))

    def __init__(self, *args, **kwargs):
        super(ReportOutdatedForm, self).__init__(*args, **kwargs)
        self.fields.pop('message')
        self.fields.pop('message_type')
        self.fields.pop('role')


class SubmitForm(forms.ModelForm):
    # media_field = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=MEDIA_CHOICES) #, verbose_name='Which types of media are you interested interested or experienced in being a source?', help_text='Choose all that apply.')

    class Meta:
        model = Person
        # fields_to_use = FIELDS_PUBLIC
        # fields_to_use.pop(-1)
        # fields_to_use.append('media_field')
        fields = FIELDS_PUBLIC
        
