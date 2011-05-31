from django.conf.urls.defaults import *
import settings
import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^fslm/', include('fslm.foo.urls')),
     (r'^move/', 'spacemanager.views.moveFiles'),
     (r'(^home/|^$)', 'spacemanager.views.home'), 
     (r'(^driveslist/)','spacemanager.views.drivesList'),
     (r'^drivestats/(?P<drivepath>.*)/$', 'spacemanager.views.drivestats'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.STATIC_URL }),
)
