import json
import urllib
import re

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.management import call_command
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.template.context import RequestContext
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode, urlencode
from django.utils.html import format_html
from django.utils.translation import ugettext as _
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from sourcelist.settings import (
    PROJECT_NAME,
    EMAIL_SENDER,
    EMAIL_HOST_USER,
    GOOGLE_RECAPTCHA_SECRET_KEY,
    SITE_URL,
)
from sources.forms import ContactForm, ReportOutdatedForm, ReportUpdateForm
from sources.models import Page, Person
from sources.tokens import account_confirmation_token

# from django.contrib.auth import login, authenticate
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.contrib.auth.models import User
# from django.core.mail import EmailMessage


# class IndexView(View):
#     """ index page """

#     def get(self, request):
#         context = {
#             'request': request,
#             'user': request.user
#         }
#         return render(request, 'index.html', context)


# class AboutView(View):
#     """ about page """

#     def get(self, request):
#         context = {
#             'request': request,
#             'user': request.user
#         }
#         return render(request, 'about.html', context)


class ConfirmView(View):
    """ confirmation URL for a user approving themself """

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        person = Person.objects.get(email_address=user.email)
        already_approved = person.approved_by_user

        if already_approved:
            message = _('You\'ve already been approved.')
            success = True
        elif user is not None and account_confirmation_token.check_token(user, token):
            ## set the Person to being approved
            person.approved_by_user = True
            person.save()
            # user.is_active = True
            # user.save()
            # login(request, user)
            # return redirect('home')
            message = _('Thank you for confirming your source profile.')
            success = True
        else:
            message = _('Confirmation link is invalid.') ## add --> Please <a href="/contact">contact us</a> so we can get you approved.
            success = False

        context = {
            'request': request,
            'message': message,
            'success': success,
            # 'user': request.user
        }

        ## see which token the user matches
        return render(request, 'confirm.html', context)


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


class PersonDetailView(DetailView):
    """ details of the Person results"""

    model = Person

    def get(self, request, *args, **kwargs):
        try:
            source = get_object_or_404(Person, id=kwargs['pk'])
        except KeyError:
            source = get_object_or_404(Person, slug=kwargs['slug'])
        try:
            url_slug = kwargs['slug']
            source_slug = source.slug
        except KeyError:
            url_slug = False
        try:
            url_id = kwargs['pk']
        except:
            url_id = False

        # if there's no slug or if slug doesn't match the person slug, we'll fix
        if not url_slug or url_slug != source_slug:
            new_url = reverse('source', kwargs={
                    'pk': source.id,
                    'slug': source.slug,
                },
            )
            if len(request.GET) > 0:
                params = urlencode(request.GET.items())
                new_url = f'{new_url}?{params}'
            return HttpResponsePermanentRedirect(new_url)
        # if there's no pk/ID in the URL, we'll fix
        elif not url_id:
            new_url = reverse('source', kwargs={
                    'pk': source.id,
                    'slug': source.slug,
                },
            )
            if len(request.GET) > 0:
                params = urlencode(request.GET.items())
                new_url += f'{new_url}?{params}'
            return HttpResponsePermanentRedirect(new_url)
        else:
            ## if it's the canonical URL
            from django.template import loader

            template = loader.get_template('sources/person_detail.html')
            context = {
                'person': source,
            }
            same_url = reverse('source', kwargs={
                    'pk': source.id,
                    'slug': source.slug,
                },
            )
            return HttpResponse(template.render(context, request))


class JoinView(View):
    """ submission of a new source """

    ## process the submitted form data
    def post(self, request, *args, **kwargs):
        form = ReportUpdateForm(request.POST)
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
                ## TK wrap in try/except and setup relevant notififcations
                # try:
                    # call_command('set_related_user', email_address)
                # except:
                    # set_related_user_failed = True
                # try:
                    # call_command('email_user', email_address, 'added')
                # except:
                    # email_user_failed = True
                ## let admin know what failed
                # if set_related_user_failed and email_user_failed:
                    # fail_type = 'both'
                # elif not set_related_user_failed and email_user_failed:
                    # fail_type = 'related_user'
                # elif set_related_user_failed not email_user_failed:
                    # fail_type = 'email_user'
                ## redirect to regular thank you page if it succeeded
                # if set_related_user_failed or email_user_failed:
                    # return HttpResponseRedirect('/thank-you/?previous=join&failed={fail_type}')
                ## otherwise redirect to thank you page with message explaning
                # else:
                return HttpResponseRedirect('/thank-you/?previous=join')
            else:
                return HttpResponseRedirect('/thank-you/?previous=join&existing=True')

    # create a blank form
    def get(self, request, *args, **kwargs):
        form = SubmitForm()
        return render(request, 'join.html', {'form': form})


class ResultsView(View):
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


def response_error_handler(request, exception):
    return render(request, '404.html', context)
handler404 = response_error_handler


class PageView(DetailView):
    """ Genericized way of creating and updating pages """

    model = Page

    def get_context_data(self, **kwargs):
        context = super(PageView, self).get_context_data(**kwargs)
        context_object_name = 'page'
        # context['now'] = timezone.now()
        return context


def RedirectSourcesURL(request):
    return redirect(reverse('index'), permanent=True)


class ReportOutdatedView(View):
    """ Report outdated profile information """
    form_class = ReportOutdatedForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # submit an email to admin
            # TODO add modified version of ReportUpdateView
            return HttpResponseRedirect('/thank-you/?previous=report-outdated')

    def get(self, request, *args, **kwargs):
        referral_url = self.request.META['HTTP_REFERER']
        url_path = referral_url.replace(SITE_URL, '')
        profile_id = re.search(r'\d+', url_path).group()  # extract first digit
        person = Person.objects.get(id=profile_id)
        initial_values = {'profile_id': profile_id}
        form = self.form_class(initial=initial_values)
        context = {
            'form': form,
            'person': person,
        }
        return render(request, 'contact.html', context)

class ReportUpdateMineView(View):
    """ Report and update your own profile """

    def get(self, request):
        """
        NOTES/OPTIONS
            - send a magic link to the user
            OR
            - provide the join form with the existing data prefilled, which they can then update and submit
                - the problem then is how we store it separately from the live one
                - e.g. subclass model to hold it then, if approved, push the changes to the original?
        """
        return render(request, 'thank-you.html')


class ReportUpdateView(View):
    """ Report update profile information for someone else """
    form_class = ReportUpdateForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            submitter_name = form_data['name']
            person_id = form_data['profile_id']
            person = Person.objects.get(id=person_id)
            person_admin_edit_path = reverse('admin:sources_person_change', args=(person.id,))
            person_admin_full_url = SITE_URL + person_admin_edit_path
            person_info_dict = [f'<p><strong>{key.title()}</strong>: {value}</p>' for key, value in form_data.items() if key != 'profile_id']
            person_info_html_string = ''.join(person_info_dict)
            person_info_html_string += f'<p><strong>Update profile:</strong> {person_admin_full_url}</p>'
            plain_message = None
            send_mail(
                'Request for update: {} from {}'.format(person, submitter_name),
                plain_message,
                EMAIL_SENDER,
                [EMAIL_HOST_USER],
                html_message=person_info_html_string,
            )
            return HttpResponseRedirect('/thank-you/?previous=report-update')

    def get(self, request, *args, **kwargs):
        # referral
        try:
            url = self.request.META['HTTP_REFERER']
            url_path = url.replace(SITE_URL, '')
        # direct
        except:
            url_path = str(self.request.get_full_path)
        profile_id = re.search(r'\d+', url_path).group()  # extract first digit
        person = Person.objects.get(id=profile_id)
        initial_values = {'profile_id': profile_id}
        form = self.form_class(initial=initial_values)
        context = {
            'form': form,
            'person': person,
        }
        return render(request, 'contact.html', context)
