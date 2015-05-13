from django.conf.urls import patterns, include, url

from copyjobs.views import IndexView,DetailView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


urlpatterns = patterns('maddt.views',
    # Examples:
     url(r'^$', 'home'),
     url(r'^db_overview/$','madison_database_overview')
)

urlpatterns += patterns('copyjobs.views',
     url(r'^copyjobs/$', IndexView.as_view(), name='index'),
     url(r'^copyjobs/(?P<pk>\d+)/$', DetailView.as_view(), name='detail'),
     url(r'^copyjobs/statistics/$','jobstatistics')
) 


    #include('maddt.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
