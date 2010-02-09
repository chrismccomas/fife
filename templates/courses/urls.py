from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from ucwv.fife.views import *
from ucwv.fife.models import *

urlpatterns = patterns('',
	(r'^$', landing_page),
	
	url(r'^course/(?P<course_id>\d+)/$', course_page, name='course_page'),
	url(r'^course/(?P<course_id>\d+)/edit/$', course_edit, name='course_edit'),
	url(r'^course/add/$', course_add, name='course_add'),
	
	# lecture forms
	url(r'^course/(?P<course_id>\d+)/add-lecture/$', lecture_add, name='lecture_add'),
	url(r'^lectures/(?P<lecture_id>\d+)/edit/$', lecture_edit, name='lecture_edit'),
	url(r'^lectures/(?P<lecture_id>\d+)/delete/$', lecture_delete, name='lecture_delete'),
	url(r'^lectures/(?P<lecture_id>\d+)/remove/$', lecture_remove, name='lecture_remove'),
	
	# required book forms
	url(r'^course/(?P<course_id>\d+)/add-book/$', book_add, name='book_add'),
	url(r'^books/(?P<book_id>\d+)/edit/$', book_edit, name='book_edit'),
	url(r'^books/(?P<book_id>\d+)/delete/$', book_delete, name='book_delete'),
	
	# announcement forms
	url(r'^course/(?P<course_id>\d+)/add-announcement/$', announcement_add, name='announcement_add'),
	url(r'^announcements/(?P<announcement_id>\d+)/edit/$', announcement_edit, name='announcement_edit'),
	url(r'^announcements/(?P<announcement_id>\d+)/delete/$', announcement_delete, name='announcement_delete'),
	url(r'^announcements/(?P<announcement_id>\d+)/$', announcement_detail, name='announcement_detail'),
	
	# accounts

	(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'fife/login.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'fife/logout.html'}),
    
    (r'^password/reset/$', 'django.contrib.auth.views.password_reset', {'template_name': 'fife/password_reset_form.html', 'email_template_name': 'fife/password_reset_email.html' } ),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'fife/password_reset_change.html',}),
	(r'^reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'fife/password_reset_done.html'}),
	(r'^reset/complete/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'fife/password_reset_complete.html'}),
	#(r'^reset/complete/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'fife/password_reset_complete.html'})

    (r'^password/change/$', 'django.contrib.auth.views.password_change', {'template_name': 'fife/password_change_form.html', }),
    (r'^password/change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'fife/password_change_done.html', }),

)