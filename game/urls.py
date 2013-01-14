from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('game.views',
    url(r'^$', 'board'),
)
