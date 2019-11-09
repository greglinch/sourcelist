from django.conf.urls import url, include
from sources.views import ConfirmView, ContactView, DetailView, ErrorView, IndexView, JoinView, PageView, ReportOutdatedView, ReportUpdateView, ResultsView, ThankYouView, SitemapView # AboutView,
from sources.helpers import search_customizations


urlpatterns = [
    ## submission form
    url(r'^confirmation/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        ConfirmView.as_view()),
    url(r'^join', JoinView.as_view()),
    url(r'^thank-you', ThankYouView.as_view()),
    ## main pages
    url(r'^$', ResultsView.as_view()),
    # url(r'^index$', ResultsView.as_view()),
    # url(r'^about$', AboutView.as_view()),
    url(r'^contact/$', ContactView.as_view()),
    url(r'^report-outdated/$', ReportOutdatedView.as_view()),
    url(r'^report-update/$', ReportUpdateView.as_view()),
    url(r'^search/', include('watson.urls', namespace='watson'), search_customizations),
    url(r'^(?P<slug>[-\w]+)/$', PageView.as_view()),
    # url(r'^results$', ResultsView.as_view()),
    url(r'^sources/(?P<slug>[-\w]+)/$', DetailView.as_view(), name='source'),
    url(r'^sitemap\.xml$', SitemapView.as_view()),
]

handler404 = ErrorView.as_view()
