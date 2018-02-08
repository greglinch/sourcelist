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
from sourcelist.settings import PROJECT_NAME, EMAIL_SENDER, EMAIL_HOST_USER
from sources.forms import ContactForm, SubmitForm
from sources.models import Page, Person
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
                EMAIL_SENDER,
                [EMAIL_HOST_USER],
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
                return HttpResponseRedirect('/thank-you/?previous=join')
            else:
                return HttpResponseRedirect('/thank-you/?previous=join&existing=True')

    # create a blank form
    def get(self, request, *args, **kwargs):
        form = SubmitForm()
        return render(request, 'join.html', {'form': form})

# class NavView(View):
#     """ nav bar """

#     def get(self, request):
#         site_name = PROJECT_NAME
#         context = site_name
#         return render(request, 'nav.html', context)

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
