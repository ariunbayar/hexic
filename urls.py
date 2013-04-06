from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', include('public.urls')),
    url(r'', include('game.urls')),
    url(r'^admin/', include('admin.urls')),
    url(r'^security/', include('security.urls')),
    url(r'^api/', include('api.urls'))
)
