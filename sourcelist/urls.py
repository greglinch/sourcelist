from django.conf import settings
from django.conf.urls import include, url
# from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = [
    ## general
    url(r'^admin/', admin.site.urls),
    ## patterns from sources app
    # url(r'^sources/', include('sources.urls')),
    url(r'^', include('sources.urls')),
    ## social auth
    url(r'^accounts/login/$', auth_views.LoginView.as_view()),
    # url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('social_django.urls')),
    url('', include('django.contrib.auth.urls')),
]

# urlpatterns += i18n_patterns(
#     ## patterns from sources app
#     # url(r'^sources/', include('sources.urls')),
#     url(r'^', include('sources.urls')),
# )

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
