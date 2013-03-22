from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('game.views',
    url(r'^game_dev/$', 'board', name='homepage'),
    url(r'^game/move/$', 'move', name='game-move'),
    url(r'^game/board/$', 'data_board', name='game-board'),
    url(r'^game/progress/$', 'progress', name='game-progress'),
)
