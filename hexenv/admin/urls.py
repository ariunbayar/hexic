from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('admin.views',
    url(r'^$', 'dashboard', name='admin-dashboard'),
    url(r'^player/show/(?P<player_id>\d+?)$', 'player_show',
        name='admin-player-show'),
    url(r'^player/new/$', 'player_new', name='admin-player-new'),
    url(r'^player/edit/(?P<player_id>\d+?)$', 'player_edit',
        name='admin-player-edit'),
    url(r'^board/show/(?P<name>[-a-z_0-9]+?)$', 'board_show', name='admin-board-show'),
    url(r'^board/new/$', 'board_new', name='admin-board-new'),
    url(r'^moves$', 'show_moves', name='show-moves'),
)
