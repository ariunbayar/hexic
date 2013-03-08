from django.conf.urls.defaults import *

urlpatterns = patterns('game_old.views',
    url(r'^$', 'home', name='homepage'),
    url(r'^game/restart$', 'game_restart', name='game-restart'),
    url(r'^game/progress/$', 'progress', name='game-progress'),
    url(r'^game/board/$', 'data_board', name='game-board'),
    url(r'^game/move/$', 'move', name='game-move'),
    #url(r'^game/select_cell/$', 'select_cell', name='select_cell'),
)
