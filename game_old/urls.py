from django.conf.urls.defaults import *

urlpatterns = patterns('game_old.views',
    url(r'^game/$', 'home', name='homepage'),
    url(r'^game/restart$', 'game_restart', name='game-restart'),
    url(r'^game/select_cell/$', 'select_cell', name='select_cell'),
)
