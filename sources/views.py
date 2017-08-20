from django.shortcuts import render
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from sources.forms import SubmitForm


def index(request):
    context = {
        'request': request,
        'user': request.user
    }
    return render(request, 'index.html', context)

def submit(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SubmitForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # form.cleaned_data
            person = form.save(commit=False)
            person.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SubmitForm()

    return render(request, 'submit.html', {'form': form})

def thankyou(request):
    context = {
        'request': request,
        'user': request.user
    }
    return render(request, 'thank-you.html', context)
