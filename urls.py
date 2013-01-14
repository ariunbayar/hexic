from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', include('public.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^game/', include('game.urls')),
    url(r'^security/', include('security.urls')),
    url(r'^api/', include('api.urls'))
)
