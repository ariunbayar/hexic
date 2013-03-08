from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'game.views.home', name='homepage'),
    url(r'^game/restart$', 'game.views.game_restart', name='game-restart'),
    url(r'^game/progress/$', 'game.views.progress', name='game-progress'),
    url(r'^game/board/$', 'game.views.data_board', name='game-board'),
    url(r'^game/move/$', 'game.views.move', name='game-move'),
    url(r'^game/select_cell/$', 'game.views.select_cell', name='select_cell'),
)
