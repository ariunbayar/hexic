from django.conf.urls import patterns, include, url


view_prefix = ''
urlpatterns = patterns(
    view_prefix,
    url(r'^$',          include('public.urls')),
    url(r'',            include('game.urls')),
    url(r'^admin/',     include('admin.urls')),
    url(r'^security/',  include('security.urls')),
    url(r'^api/',       include('api.urls')),
)
