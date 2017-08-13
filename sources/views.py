from django.shortcuts import render
from django.template.context import RequestContext


def index(request):
    context = {
        'request': request,
        'user': request.user
    }
    return render(request, 'index.html', context)