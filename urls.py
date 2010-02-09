from django.conf import settings
from django.conf.urls.defaults import *
 
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

	(r'^', include('fife.courses.urls')),
	
	(r'^admin/', include(admin.site.urls)),
	#(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
