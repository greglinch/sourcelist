from django.forms import ModelForm
from sources.models import Person


class SubmitForm(ModelForm):
	class Meta:
		model = Person
		fields = ['prefix', 'first_name', 'middle_name', 'last_name', 'title', 'organization', 'website', 'expertise', 'email_address', 'phone_number_primary', 'phone_number_secondary', 'notes', 'language', 'timezone', 'city', 'state', 'country', 'status']