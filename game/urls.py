from django.conf.urls import patterns, url


view_prefix = 'game.views'
urlpatterns = patterns(
    view_prefix,
    url(r'^game/play/$',         'play'),
    url(r'^game/dashboard/$',    'dashboard'),
    url(r'^game/quick_match/$',  'quick_match'),
    url(r'^game/auto_login/$',   'auto_login'),  # TODO debug only
)
