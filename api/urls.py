from django.conf.urls import patterns, url

view_prefix = ''
urlpatterns = patterns(
    view_prefix,
    url(r'^$', 'api.views.message_received'),
    # interface for game server
    url(r'^_game_server', 'api.views.game_server'),
)
