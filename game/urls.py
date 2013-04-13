from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('game.views',
    url(r'^game/play/$', 'play'),
    url(r'^game/move/$', 'move'),
    url(r'^game/board/$', 'data_board'),
    url(r'^game/progress/$', 'progress'),
    url(r'^game/dashboard/$', 'dashboard'),
    # TODO remove
    url(r'^game/select_cell/$', 'select_cell'),
)
