from django.conf.urls.defaults import patterns, include
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    (r'', include('game.urls')),
    (r'^admin/', include('admin.urls')),
    (r'', include('player.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
    #(r'^backend/', include(admin.site.urls)),
)
