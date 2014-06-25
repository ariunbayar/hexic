from django.conf.urls import patterns, url


view_prefix = ''
urlpatterns = patterns(
    view_prefix,
    url(r'^login$',  'security.views.login'),
    url(r'^logout$', 'security.views.logout'),
)
