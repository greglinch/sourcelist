from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from sources.views import index
from sourcelist import settings


urlpatterns = [
	url(r'^sources/', include('sources.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', auth_views.LoginView.as_view()),
    # ## social auth
    url(r'^$', index, name='index'),
    # url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('social_django.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
