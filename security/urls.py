from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('',
    url(r'^login$', 'security.views.login'),
    url(r'^logout$', 'security.views.logout'),
)
