from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = [
    ## patterns from sources app
	# url(r'^sources/', include('sources.urls')),
    url(r'^', include('sources.urls')),
    ## general
    url(r'^admin/', admin.site.urls),
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
