from django.conf.urls.defaults import patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'startproject.views.home', name='home'),
    # url(r'^startproject/', include('startproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url('', 'login.views.index'),
)
