from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'api.views.new_msg'),
)
