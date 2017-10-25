from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.management import call_command
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render # , redirect
from django.template.context import RequestContext
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.html import format_html
from django.views import View
from django.views.generic.detail import DetailView #, ListView
from sourcelist.settings import PROJECT_NAME
from sources.forms import ContactForm, SubmitForm
from sources.models import Person
from sources.tokens import account_confirmation_token
# from django.contrib.auth import login, authenticate
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.contrib.auth.models import User
# from django.core.mail import EmailMessage


class IndexView(View):
    """ index page """

    def get(self, request):
        context = {
            'request': request,
            'user': request.user
        }
        return render(request, 'index.html', context)

class AboutView(View):
    """ about page """

    def get(self, request):
        context = {
            'request': request,
            'user': request.user
        }
        return render(request, 'about.html', context)

class ConfirmView(View):
    """ trigger mgmt cmd or, ideally, just the related function or just put the code here! """

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_confirmation_token.check_token(user, token):
            ## set the Person to being approved
            person = Person.objects.get(email_address=user.email)
            person.approved_by_user = True
            person.save()
            # user.is_active = True
            # user.save()
            # login(request, user)
            # return redirect('home')
            return HttpResponse('Thank you for confirming your source profile.') # Now you can view the live entry {}.').format(live_url)
        else:
            return HttpResponse('Confirmation link is invalid!')

        ## see which token the user matches
        return render(request, 'confirmation.html', context)

class ContactView(View):
    """ contact page """

    ## process the submitted form data
    def post(self, request, *args, **kwargs):
    # if request.method == 'POST':
        form = ContactForm(request.POST)
        ## check whether it's valid:
        if form.is_valid():
            ## extract the necessary value for sending emails
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            name = form.cleaned_data['name']
            plain_message = ''
            html_message = '<table> \
                <tr><td>Name:</td><td>{}</td></tr> \
                <tr><td>Email:</td><td>{}</td></td></tr> \
                <tr><td>Message:</td><td>{}</td></td></tr> \
                </table> \
                '.format(name, email, message)
            send_mail(
                '[{}] Contact form messsage from {}'.format(PROJECT_NAME, name),
                plain_message,
                'greglinch@gmail.com',
                ['greglinch@gmail.com'],
                html_message=html_message,
                )
            # redirect to thank you page:
            return HttpResponseRedirect('/thank-you/')

    # create a blank form
    def get(self, request, *args, **kwargs):
        form = ContactForm()
        return render(request, 'contact.html', {'form': form})

class DetailView(DetailView):
    """ details of the Person results"""

    model = Person
    # context_object_name = 'person'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context_object_name = 'person'
        # context['now'] = timezone.now()
        return context

    # def get_queryset(self):
    #     queryset = Person.objects.filter(slug=self.slug)
    #     return queryset

    # def get(self, request):

    #     person = Person.objects.filter(
    #         slug=slug
    #     ).values()

    #     context = {
    #         'person': person
    #     }

    #     return render(request, 'detail.html', context) # , {'form': form})

class JoinView(View):
    """ submission of a new source """

    ## process the submitted form data
    def post(self, request, *args, **kwargs):
    # if request.method == 'POST':
        form = SubmitForm(request.POST)
        ## check whether it's valid:
        if form.is_valid():
            ## extract the necessary values for sending emails
            # status = form.cleaned_data['status'].split('_')[0]
            email_address = form.cleaned_data['email_address']
            try:
                existing = Person.objects.get(email_address=email_address)
            except:
                existing = False
            if not existing:
                ## save the form data
                form.save()
                ## set the related user and email the source
                call_command('set_related_user', email_address)
                call_command('email_user', email_address, 'added')
                # redirect to thank you page:
                return HttpResponseRedirect('/thank-you/')
            else:
                return HttpResponseRedirect('/thank-you/?existing=True')

    # create a blank form
    def get(self, request, *args, **kwargs):
        form = SubmitForm()
        return render(request, 'join.html', {'form': form})

class ResultsView(View):
# class ResultsView(ListView):
    """ search and display results"""

    def get(self, request):
        # query = request.GET['q']

        field_list = ['last_name', 'first_name', 'type_of_scientist', 'expertise', 'organization', ]

        results = Person.objects.filter(
            approved_by_user=True,
            approved_by_admin=True
        ).values() # values(*field_list)

        context = {
            'field_list': field_list,
            'results': results
        }

        return render(request, 'results.html', context) # , {'form': form})

class ThankYouView(View):
    """ thank you page after submission """

    def get(self, request):
        existing = request.GET.get('existing')
        context = {
            'request': request,
            'existing': existing
            # 'user': request.user
        }
        return render(request, 'thank-you.html', context)
