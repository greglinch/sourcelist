from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from sources.views import about, confirm, contact, index, join, thankyou


urlpatterns = [
    ## patterns from sources app
	url(r'^sources/', include('sources.urls')),
    ## general
    url(r'^admin/', admin.site.urls),
    ## site pages
    url(r'^$', index, name='index'),
    url(r'^index$', index, name='index'),
    url(r'^about$', about, name='about'),
    url(r'^contact$', contact, name='contact'),
    ## submission form
    url(r'^confirmation/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        confirm, name='confirm'), ## UPDATE?!?!
    url(r'^join', join, name='join'),
    url(r'^thank-you', thankyou, name='thank-you'),
    ## social auth
    url(r'^accounts/login/$', auth_views.LoginView.as_view()),
    # url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('social_django.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
