from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('board.views',
    url(r'^new/$', 'board_new', name='board-new'),
    url(r'^show/(?P<name>\w+?)/(?P<position>\d+?)/$', 'board_show',
        name='board-show'),
    url(r'^save/(?P<name>\w+?)/(?P<position>\d+?)/$', 'board_save',
        name='board-save'),
)
