from django.conf.urls.defaults import *
import settings
import os

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     (r'^move/', 'spacemanager.views.moveFiles'),
     (r'(^home/|^$)', 'spacemanager.views.home'), 
     (r'(^driveslist/)','spacemanager.views.drivesList'),
     (r'^drivestats/(?P<drivepath>.*)/$', 'spacemanager.views.drivestats'),
     (r'^initDbQueue/$', 'spacemanager.views.initQueue'),
     (r'^settings/$', 'spacemanager.views.settings'),
     (r'^drivewizard/$', 'spacemanager.views.drivewizard'),
     url(r'^viewFileInDbQueue/$', 'spacemanager.views.viewDbQueue',name='dbQueue'),
     (r'^viewTasksInDbQueue/$', 'spacemanager.views.viewActiveDbQueue'),
     (r'^deleteQueueItem/(?P<queueid>\d+)/$', 'spacemanager.views.deleteQueueItem'),
     (r'^admin/', include(admin.site.urls)),
     (r'^login/$',  'django.contrib.auth.views.login'), 
     (r'^logout/$',  'spacemanager.views.logmeout')
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.STATIC_URL }),
)
