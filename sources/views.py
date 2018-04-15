from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.management import call_command
from django.http import HttpResponse, HttpResponseRedirect#, Http404
from django.shortcuts import render # , redirect
from django.template.context import RequestContext
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.html import format_html
from django.utils.translation import ugettext as _
from django.views import View
from django.views.generic.detail import DetailView #, ListView
from django.views.generic.edit import FormView
from sourcelist.settings import PROJECT_NAME, EMAIL_SENDER, EMAIL_HOST_USER, GOOGLE_RECAPTCHA_SECRET_KEY
from sources.forms import ContactForm, SubmitForm
from sources.models import Page, Person
from sources.tokens import account_confirmation_token
import json
import urllib
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


# class AboutView(View):
#     """ about page """

#     def get(self, request):
#         context = {
#             'request': request,
#             'user': request.user
#         }
#         return render(request, 'about.html', context)


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
            output = _('Thank you for confirming your source profile.')
            return HttpResponse(output) # Now you can view the live entry {}.').format(live_url)
        else:
            output = _('Confirmation link is invalid!')
            return HttpResponse(output)

        ## see which token the user matches
        return render(request, 'confirmation.html', context)


class ContactView(FormView):
    """ contact page """
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/thank-you/'

    def form_valid(self, form):
        ## reCAPTCHA validation
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req =  urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        ## extract the necessary value for sending emails
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        role = form.cleaned_data['role']
        message = form.cleaned_data['message']
        message_type = form.cleaned_data['message_type']
        message_type_display = dict(form.fields['message_type'].choices)[message_type]
        ## construct the message
        plain_message = ''
        html_message = '<table> \
            <tr><td>Name:</td><td>{}</td></tr> \
            <tr><td>Email:</td><td>{}</td></td></tr> \
            <tr><td>Role:</td><td>{}</td></td></tr> \
            <tr><td>Message:</td><td>{}</td></td></tr> \
            </table> \
            '.format(name, email, role, message)
        ## send the message
        if result['success']:
            send_mail(
                '[{} contact form] {} from {}'.format(PROJECT_NAME, message_type_display, name),
                plain_message,
                EMAIL_SENDER,
                [EMAIL_HOST_USER],
                html_message=html_message,
            )
        ## or return the form with the same values plus the error
        else:
            payload = {
                'form': form,
                'captcha_error': True
            }
            return render(self.request, 'contact.html', payload)

        return super().form_valid(form)


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
                return HttpResponseRedirect('/thank-you/?previous=join')
            else:
                return HttpResponseRedirect('/thank-you/?previous=join&existing=True')

    # create a blank form
    def get(self, request, *args, **kwargs):
        form = SubmitForm()
        return render(request, 'join.html', {'form': form})


class ResultsView(View):
# class ResultsView(ListView):
    """ search and display results"""

    def get(self, request):
        # query = request.GET['q']

        field_list = ['first_name', 'last_name', 'type_of_expert', 'expertise', 'organization', ]

        results = Person.objects.filter(
            approved_by_user=True,
            approved_by_admin=True,
            role='source'
        ).values() # values(*field_list)

        context = {
            'field_list': field_list,
            'results': results
        }

        return render(request, 'results.html', context) # , {'form': form})


class SitemapView(View):
    """ sitemap for search engines """

    def get(self, request):
        context = {
            'request': request,
            # 'user': request.user
        }
        return render(request, 'sitemap.xml', context)


class ThankYouView(View):
    """ thank you page after submission """

    def get(self, request):
        existing = request.GET.get('existing')
        previous = request.GET.get('previous')
        context = {
            'request': request,
            'existing': existing,
            'previous': previous
            # 'user': request.user
        }
        return render(request, 'thank-you.html', context)


class ErrorView(View):
    """ 404 page """

    def get(self, request):
        return render(request, '404.html', context)


class PageView(DetailView):
    """ Genericized way of creating and updating pages """

    model = Page

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context_object_name = 'page'
        # context['now'] = timezone.now()
        return context
