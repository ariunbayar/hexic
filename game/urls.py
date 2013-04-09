from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('game.views',
    url(r'^game_dev/$', 'board', name='homepage'),
    url(r'^game/move/$', 'move', name='game-move'),
    url(r'^game/board/$', 'data_board', name='game-board'),
    url(r'^game/progress/$', 'progress', name='game-progress'),
    url(r'^game/select_cell/$', 'select_cell', name='select_cell'),
    url(r'^game/select_board/$', 'select_board', name='select_board'),
)
