from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to
from django.views.generic import list_detail

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^', include('ucwv.fife.urls')),
	(r'^admin/', include(admin.site.urls)),
	#(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
