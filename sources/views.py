from django.core.management import call_command
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render # , redirect
from django.template.context import RequestContext
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_confirmation_token
from sources.forms import SubmitForm
# from django.contrib.auth import login, authenticate
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.contrib.auth.models import User
# from django.core.mail import EmailMessage


def index(request):
    """ index page """

    context = {
        'request': request,
        'user': request.user
    }
    return render(request, 'index.html', context)

def confirm(request, uidb64, token):
    """ trigger mgmt cmd or, ideally, just the related function or just put the code here! """

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for confirming this source profile.') # Now you can view the live entry {}.').format(live_url)
    else:
        return HttpResponse('Activation link is invalid!')

    ## see which token the user matches
    return render(request, 'confirmation.html', context)

def submit(request):
    """ submission of a new source """

    ## if this is a POST request we need to process the form data
    if request.method == 'POST':
        ## create a form instance and populate it with data from the request:
        form = SubmitForm(request.POST)
        ## check whether it's valid:
        if form.is_valid():
            ## extract the necessary values for sending emails
            status = form.cleaned_data['status'].split('_')[0]
            email_address = form.cleaned_data['email_address']
            ## save the form data
            form.save()
            ## set the related user and email the source
            call_command('set_related_user', email_address)
            call_command('email_user', email_address, status)
            # redirect to thank you page:
            return HttpResponseRedirect('/thank-you/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = SubmitForm()

    return render(request, 'submit.html', {'form': form})

def thankyou(request):
    """ thank you page after submission """

    context = {
        'request': request,
        'user': request.user
    }
    return render(request, 'thank-you.html', context)
