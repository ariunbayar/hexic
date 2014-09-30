from django.conf.urls import patterns, url


view_prefix = 'admin.views'
urlpatterns = patterns(
    view_prefix,
    url(r'^accounts$',                       'accounts'),
    url(r'^account/add$',                    'add_acc'),
    url(r'^account/(?P<acc_id>\d+)/update$', 'update_acc'),
    url(r'^account/(?P<acc_id>\d+)/delete$', 'del_acc'),
    url(r'^admins$',                         'admins'),
    url(r'^admin/add$',                      'add_admin'),
    url(r'^admin/(?P<admin_id>\d+)/update$', 'update_admin'),
    url(r'^admin/(?P<admin_id>\d+)/delete$', 'del_admin'),
    url(r'^logout$',                         'logout'),
    url(r'^messages$',                       'messages'),
    url(r'^login$',                          'login'),
    url(r'^dashboard$',                      'dashboard'),
)
