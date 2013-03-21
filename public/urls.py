from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('public.views',
    url(r'^$', 'index'),
)
