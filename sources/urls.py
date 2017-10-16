from django.conf.urls import url
from sources.views import AboutView, ConfirmView, ContactView, IndexView, JoinView, ResultsView, ThankYouView


urlpatterns = [
	## main pages
    url(r'^$', IndexView.as_view()),
    url(r'^index$', IndexView.as_view()),
    url(r'^about$', AboutView.as_view()),
    url(r'^contact$', ContactView.as_view()),
    url(r'^results$', ResultsView.as_view()),
    ## submission form
    url(r'^confirmation/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        ConfirmView.as_view()),
    url(r'^join', JoinView.as_view()),
    url(r'^thank-you', ThankYouView.as_view()),
]