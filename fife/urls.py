from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from ucwv.fife.views import *
from ucwv.fife.models import *

urlpatterns = patterns('',
	(r'^$', landing_page),
	
	url(r'^resources/$', resources, name='resources'),
	url(r'^error/$', error_page, name='error_page'),
	
	url(r'^faculty/(?P<faculty_id>\d+)/$', faculty_info, name='faculty_info'),
	url(r'^faculty/(?P<faculty_id>\d+)/edit/$', faculty_edit, name='faculty_edit'),
	
	url(r'^course/(?P<course_id>\d+)/$', course_page, name='course_page'),
	url(r'^course/(?P<course_id>\d+)/edit/$', course_edit, name='course_edit'),
	url(r'^course/add/$', course_add, name='course_add'),
	
	# lecture forms
	url(r'^course/(?P<course_id>\d+)/add-lecture/$', lecture_add, name='lecture_add'),
	url(r'^lectures/(?P<lecture_id>\d+)/edit/$', lecture_edit, name='lecture_edit'),
	url(r'^lectures/(?P<lecture_id>\d+)/delete/$', lecture_delete, name='lecture_delete'),
	url(r'^lectures/(?P<lecture_id>\d+)/remove/$', lecture_remove, name='lecture_remove'),
	
	# resources forms
	url(r'^course/(?P<course_id>\d+)/add-resource/$', resource_add, name='resource_add'),
	url(r'^resources/(?P<resource_id>\d+)/edit/$', resource_edit, name='resource_edit'),
	url(r'^resources/(?P<resource_id>\d+)/delete/$', resource_delete, name='resource_delete'),
	
	# required book forms
	url(r'^course/(?P<course_id>\d+)/add-book/$', book_add, name='book_add'),
	url(r'^books/(?P<book_id>\d+)/edit/$', book_edit, name='book_edit'),
	url(r'^books/(?P<book_id>\d+)/delete/$', book_delete, name='book_delete'),
	
	# announcement forms
	url(r'^course/(?P<course_id>\d+)/add-announcement/$', announcement_add, name='announcement_add'),
	url(r'^announcements/(?P<announcement_id>\d+)/edit/$', announcement_edit, name='announcement_edit'),
	url(r'^announcements/(?P<announcement_id>\d+)/delete/$', announcement_delete, name='announcement_delete'),
	url(r'^announcements/(?P<announcement_id>\d+)/$', announcement_detail, name='announcement_detail'),
	
	# audio uploads
	url(r'^audio/upload/$', audio_upload, name='audio_upload'),
	url(r'^audio/edit/(?P<audio_id>\d+)/$', audio_edit, name='audio_edit'),
	url(r'^audio/delete/(?P<audio_id>\d+)/$', audio_delete, name='audio_delete'),
	url(r'^audio/upload/complete/$', audio_uploaded, name='audio_uploaded'),
)