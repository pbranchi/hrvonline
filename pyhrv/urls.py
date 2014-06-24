from django.conf.urls import patterns, include, url

from django.contrib import admin
from .views import (MainView, process_key, submit_jobs, start_process, stop_process)
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pyhrv.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(regex='^$', view=MainView, name='home'),
    
    url(regex='^process_key/$',  view=process_key, name='process_key'),
    url(regex='^submit_jobs/$', view=submit_jobs, name='submit_jobs'),
    url(regex='^start_job/$', view=start_process, name='start_process'),
    url(regex='^stop_job/$', view=stop_process, name='stop_process'),
)
