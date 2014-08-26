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
    url(r'^game/quick_match/$',  'quick_match'),
    # TODO remove
    url(r'^game/select_cell/$',  'select_cell'),
    url(r'^game/auto_login/$',   'auto_login'),  # TODO debug only
)
