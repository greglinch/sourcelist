from django import forms
from sources.models import Person
# from sources.choices import MEDIA_CHOICES


FIELDS_PUBLIC = ['prefix', 'pronouns', 'first_name', 'middle_name', 'last_name', 'type_of_expert', 'title', 'organization', 'website', 'expertise', 'email_address', 'phone_number_primary', 'phone_number_secondary', 'skype', 'twitter', 'language', 'timezone', 'city', 'state', 'country', 'notes', 'media_audio', 'media_text', 'media_video']

class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(
        required=True,
        widget=forms.Textarea
    )

class SubmitForm(forms.ModelForm):
    # media_field = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=MEDIA_CHOICES) #, verbose_name='Which types of media are you interested interested or experienced in being a source?', help_text='Choose all that apply.')

    class Meta:
        model = Person
        # fields_to_use = FIELDS_PUBLIC
        # fields_to_use.pop(-1)
        # fields_to_use.append('media_field')
        fields = FIELDS_PUBLIC
        
