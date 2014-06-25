from django.conf.urls import patterns, url


view_prefix = 'game.views'
urlpatterns = patterns(
    view_prefix,
    url(r'^game/play/$',         'play'),
    url(r'^game/move/$',         'move'),
    url(r'^game/board/$',        'data_board'),
    url(r'^game/progress/$',     'progress'),
    url(r'^game/dashboard/$',    'dashboard'),
    url(r'^game/select_board/$', 'select_board'),
    # TODO remove
    url(r'^game/select_cell/$',  'select_cell'),
)
