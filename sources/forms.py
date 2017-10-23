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
        fields = ['prefix', 'first_name', 'middle_name', 'last_name', 'type_of_scientist', 'title', 'organization', 'website', 'expertise', 'email_address', 'phone_number_primary', 'phone_number_secondary', 'language', 'timezone', 'city', 'state', 'country', 'notes']
