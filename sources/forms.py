from django import forms
from sources.models import Person


class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(
        required=True,
        widget=forms.Textarea
    )

class SubmitForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['prefix', 'pronouns', 'first_name', 'middle_name', 'last_name', 'type_of_expert', 'title', 'organization', 'website', 'expertise', 'email_address', 'phone_number_primary', 'phone_number_secondary', 'twitter', 'language', 'timezone', 'city', 'state', 'country', 'notes']
