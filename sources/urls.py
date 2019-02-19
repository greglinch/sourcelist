from django.conf.urls import url, include
from django.urls import path

from sources.views import (
    ConfirmView,
    ContactView,
    PersonDetailView,
    JoinView,
    PageView,
    RedirectSourcesURL,
    ResultsView,
    SitemapView,
    ThankYouView,
)
from sources.helpers import search_customizations


urlpatterns = [
    ## submission form
    url(r'^confirmation/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        ConfirmView.as_view()),
    # these go before pages with vars in the urls to avoid confusion
    url(r'^join', JoinView.as_view()),
    url(r'^thank-you', ThankYouView.as_view()),
    ## main pages
    url(r'^$', ResultsView.as_view(), name='index'),
    url(r'^contact/$', ContactView.as_view()),
    url(r'^search/', include('watson.urls', namespace='watson'), search_customizations),
    url(r'^sources/$', RedirectSourcesURL),
    path('<slug:slug>/', PageView.as_view()),
    path('sources/<int:pk>/', PersonDetailView.as_view()),
    path('sources/<slug:slug>/', PersonDetailView.as_view()),
    path('sources/<int:pk>/<slug:slug>/', PersonDetailView.as_view(), name='source'),
    url(r'^sitemap\.xml$', SitemapView.as_view()),
]

handler404 = 'sources.views.ErrorView'
