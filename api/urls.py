from django.conf.urls import patterns, url

view_prefix = ''
urlpatterns = patterns(
    view_prefix,
    url(r'^$', 'api.views.message_received'),
)
