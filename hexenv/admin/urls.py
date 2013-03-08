from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^admin/board$', 'admin.views.show_board', name='admin-board'),
    url(r'^admin/moves$', 'admin.views.show_moves', name='admin-moves'),
)
