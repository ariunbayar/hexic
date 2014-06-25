from django.conf.urls import patterns, url


view_prefix = 'public.views'
urlpatterns = patterns(
    view_prefix,
    url(r'^$', 'index'),
)
