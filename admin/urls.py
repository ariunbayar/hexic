from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('admin.views',
    url(r'^accounts$', 'accounts'),
    url(r'^account/add$', 'add_acc'),
    url(r'^account/update$', 'update_acc'),
    url(r'^account/delete$', 'del_acc'),
    url(r'^admins$', 'admins'),
    url(r'^logout$', 'logout'),
    url(r'^messages$', 'messages'),
    url(r'^login$', 'login'),
)
