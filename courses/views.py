import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context
from django.forms.models import modelformset_factory, inlineformset_factory
from django.views.generic.list_detail import object_list
from django.contrib.auth.models import User, Group
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q

from fife.courses.models import *
from fife.courses.forms import *

def landing_page(request):
	if request.user.is_authenticated():
		
		# if in Students group
		if [x for x in request.user.groups.all() if x.pk in [9]]:
			
			courses = Course.objects.filter(term__active=True, classyear__group__user=request.user)
			
			term = Term.objects.get(active=1)
			lectures = Lecture.lecture_live.filter(course__in=courses).order_by('-lecture_date')[:5]
			audio = Audio.audio_live.filter(course__in=courses).order_by('-audio_date')[:5]
			announcements = Announcement.announcement_live.filter(course__in=courses).order_by('-created_date')[:5]
			sidebar = SidebarLinks.objects.filter(sidebar=3).order_by('order')
			
			return render_to_response('fife/student_index.html', {'courses': courses, 'lectures': lectures, 'audio': audio, 'announcements': announcements, 'sidebar': sidebar}, context_instance=RequestContext(request))
			
		# if in Faculty group
		elif [x for x in request.user.groups.all() if x.pk in [1]]:
			
			faculty = Faculty.objects.get(user=request.user)
			if request.user.pk == 1 or request.user.pk == 442 or request.user.pk == 3:
				course = Course.objects.filter(term__active=True)
			else:
				course = Course.objects.filter(Q(course_coordinator=faculty) | Q(instructor=faculty), term__active=True).distinct() 


			if request.user.pk == 1 or request.user.pk == 3:
				sam = True
			else:
				sam = False

			lectures = Lecture.lecture_live.filter(user=request.user.pk).order_by('-lecture_date')[:5]
			announcements = Announcement.announcement_live.filter(user=request.user.pk).order_by('-created_date')[:5]
			sidebar = SidebarLinks.objects.filter(sidebar=1).order_by('order')
		
			return render_to_response('fife/faculty_index.html', {'faculty': faculty, 'course': course, 'sidebar': sidebar, 'sam': sam,}, context_instance=RequestContext(request))
		
		# if in neither Faculty or Students group
		else:
			return HttpResponseRedirect('/fife/error/')
			
	else:
		return HttpResponseRedirect('/mayberry/login/')
		
def course_page(request, course_id):
	if request.user.is_authenticated():
		
		if [x for x in request.user.groups.all() if x.pk in [9]]:
			
			course = Course.objects.get(pk=course_id)
			
			book = RequiredBook.book_live.filter(course=course_id)
			announcement = Announcement.announcement_live.filter(course=course_id).order_by('-created_date')
			lecture = Lecture.lecture_live.filter(course=course_id).order_by('-lecture_date', '-created_date')
			audio = Audio.audio_live.filter(course=course_id).order_by('-audio_date')
			term = Term.objects.get(active=1)
			sidebar = SidebarLinks.objects.filter(sidebar=3).order_by('order')
			resources = Resource.resource_live.filter(course=course_id).order_by('-created_date')
			
			try:
				alerts = EmailAlerts.objects.get(user=request.user, course=course_id)
			except EmailAlerts.DoesNotExist:
				alerts = EmailAlerts()
				alerts.user = User.objects.get(pk=request.user.pk)
				alerts.course = Course.objects.get(pk=course_id)
				alerts.announcement_alert = True
				alerts.audio_alert = True
				alerts.lecture_alert = True
				alerts.save()
			
			if request.method == "POST":			
				form = AlertForm(request.POST, instance=alerts)
				if form.is_valid():
					alert = form.save(commit=False)
					alert.save()

					return HttpResponseRedirect('/fife/course/%s/' % course.pk)
			else:
				form = AlertForm(instance=alerts)
		
			return render_to_response('fife/student_course.html', {'resources': resources, 'course': course, 'books': book, 'announcements': announcement, 'lectures': lecture, 'term': term, 'audio': audio, 'sidebar': sidebar, 'form': form,}, context_instance=RequestContext(request))
			
		elif [x for x in request.user.groups.all() if x.pk in [1]]:
			
			course = Course.objects.get(pk=course_id)
			book = RequiredBook.book_live.filter(course=course_id)
			announcement = Announcement.announcement_live.filter(course=course_id).order_by('-created_date')
			lecture = Lecture.lecture_live.filter(course=course_id).order_by('-lecture_date', '-created_date')
			audio = Audio.audio_live.filter(course=course_id).order_by('-audio_date')
			term = Term.objects.get(active=1)
			sidebar = SidebarLinks.objects.filter(sidebar=1).order_by('order')
			faculty = Faculty.objects.get(user=request.user)
			resources = Resource.resource_live.filter(course=course_id).order_by('-created_date')
			
			if request.user.pk == 1 or request.user.pk == 3:
				sam = True
			else:
				sam = False
				
			if faculty in course.instructor.all() or faculty in course.course_coordinator.all() or request.user.pk == 1 or request.user.pk == 442 or request.user.pk == 3:
				return render_to_response('fife/faculty_course.html', {'resources': resources, 'sam': sam, 'course': course, 'books': book, 'announcements': announcement, 'lectures': lecture, 'term': term, 'audio': audio, 'sidebar': sidebar, 'faculty': faculty,}, context_instance=RequestContext(request))
			else:
				return HttpResponseRedirect('/fife/error/')
		else:
			return HttpResponseRedirect('/fife/error/')
	else:
		return HttpResponseRedirect('/mayberry/login/')
		
def course_edit(request, course_id):
	if request.user.is_authenticated():
		
		faculty = Faculty.objects.get(user=request.user)
		sidebar = SidebarLinks.objects.filter(sidebar=1).order_by('order')
		
		try:
			course = Course.objects.get(pk=course_id)
			if faculty in course.instructor.all() or faculty in course.course_coordinator.all() or request.user.pk == 1 or request.user.pk == 442:
				if request.method == "POST":			
					course_form = CourseForm(request.POST, request.FILES, instance=course)
					if course_form.is_valid():	
						course_form.save()		
						return HttpResponseRedirect('http://sop.ucwv.edu/fife/course/%s/' % course.pk)
						
				else:
					course_form = CourseForm(instance=course)
					
				return render_to_response('fife/faculty_course_edit.html', {'course_form': course_form, 'course': course, 'sidebar': sidebar, 'faculty': faculty,},
								context_instance=RequestContext(request))
			else:
				return HttpResponseRedirect('/fife/error/')
		except Course.DoesNotExist:
			return HttpResponseRedirect('/fife/error/')
	
	else:
		return HttpResponseRedirect('/mayberry/login/')
		
def course_add(request):
	if request.user.is_authenticated():
		
		faculty = Faculty.objects.get(user=request.user)
		sidebar = SidebarLinks.objects.filter(sidebar=1).order_by('order')
			
		if request.method == "POST":			
			course_form = AddCourseForm(request.POST, request.FILES)
			if course_form.is_valid():
				new_course = course_form.save(commit=False)
				new_course.save()
				
				# alerts
						
				course_form.save_m2m()
				
				return HttpResponseRedirect('http://sop.ucwv.edu/fife/course/%s/' % new_course.pk)
					
		else:
			course_form = AddCourseForm()
			
		return render_to_response('fife/faculty_course_add.html', {'course_form': course_form, 'sidebar': sidebar},
							context_instance=RequestContext(request))
	
	else:
		return HttpResponseRedirect('/mayberry/login/')
		
def announcement_detail(request, announcement_id):
	if request.user.is_authenticated():
		
		if [x for x in request.user.groups.all() if x.pk in [9]]:
			
			announcement = Announcement.objects.get(pk=announcement_id)
			sidebar = SidebarLinks.objects.filter(sidebar=3).order_by('order')
			
			return render_to_response('fife/student_announcement.html', {'announcement': announcement, 'sidebar': sidebar}, context_instance=RequestContext(request))
			
		elif [x for x in request.user.groups.all() if x.pk in [1]]:
			
			announcement = Announcement.objects.get(pk=announcement_id)
			sidebar = SidebarLinks.objects.filter(sidebar=1).order_by('order')
			faculty = Faculty.objects.get(user=request.user)
			
			return render_to_response('fife/faculty_announcement.html', {'announcement': announcement, 'sidebar': sidebar, 'faculty': faculty,}, context_instance=RequestContext(request))
		else:
			return HttpResponseRedirect('/fife/error/')	
		
	else:
		return HttpResponseRedirect('/mayberry/login/')
		
def announcement_add(request, course_id):
	if request.user.is_authenticated():
		
		if [x for x in request.user.groups.all() if x.pk in [1]]:
			
			course = Course.objects.get(pk=course_id)
			sidebar = SidebarLinks.objects.filter(sidebar=1).order_by('order')
			faculty = Faculty.objects.get(user=request.user)
			
			if request.method == "POST":			
				form = AddAnnouncementForm(request.POST)
				if form.is_valid():
					new_announcement = form.save(commit=False)
					new_announcement.user = request.user
					new_announcement.course = Course.objects.get(pk=course_id)
					new_announcement.active = True
					new_announcement.save()
					
					alert = EmailAlerts.objects.filter(course=course_id, announcement_alert=True,)
					for student in alert:
						subject = "New Announcement Posted for %s" % (course.short)
						recipients = [student.user.email]
						#recipients = ['pharmacy-faculty@ucwv.edu', 'pharmacy-staff@ucwv.edu']
						sender = 'sopwebmail@ucwv.edu'

						text_content = loader.get_template('fife/alerts_announcement.txt')
						html_content = loader.get_template('fife/alerts_announcement.html')
						c = Context({
							'course': course,
							'new_announcement': new_announcement,
							'student': student,
						})

						msg = EmailMultiAlternatives(subject, text_content.render(c), sender, recipients,)
						msg.attach_alternative(html_content.render(c), "text/html")
						msg.send()
					
					
					
					return HttpResponseRedirect('/fife/course/%s/' % course.pk)
			else:
				form = AddAnnouncementForm()

			return render_to_response('fife/faculty_add_announcement.html', {'form': form, 'course': course, 'sidebar': sidebar, 'faculty': faculty}, context_instance=RequestContext(request))
			
		else:
			return HttpResponseRedirect('/fife/error/')
		
	else:
		return HttpResponseRedirect('/mayberry/login/')
		
def announcement_edit(request, announcement_id):
	if request.user.is_authenticated():

		if [x for x in request.user.groups.all() if x.pk in [1]]:

			announcement = Announcement.objects.get(pk=announcement_id)
			course = Course.objects.get(pk=announcement.course.pk)
			sidebar = SidebarLinks.objects.filter(sidebar=1).order_by('order')
			faculty = Faculty.objects.get(user=request.user)
			
			if request.method == "POST":			
				form = AddAnnouncementForm(request.POST, instance=announcement)
				if form.is_valid():
					form.save()

					return HttpResponseRedirect('/fife/course/%s/' % course.pk)
			else:
				form = AddAnnouncementForm(instance=announcement)
				
			return render_to_response('fife/faculty_edit_announcement.html', {'form': form, 'course': course, 'announcement': announcement, 'sidebar': sidebar, 'faculty': faculty,}, context_instance=RequestContext(request))	
		
		else:
			return HttpResponseRedirect('/fife/error/')	

	else:
		return HttpResponseRedirect('/mayberry/login/')
		
def announcement_delete(request, announcement_id):
	announcement = Announcement.objects.get(pk=announcement_id)
	course = Course.objects.get(pk=announcement.course.pk)
	announcement.active = False
	announcement.save()

	return HttpResponseRedirect('/fife/course/%s' % course.pk)
		
def lecture_add(request, course_id):
	if request.user.is_authenticated():

		if [x for x in request.user.groups.all() if x.pk in [1]]:

			course = Course.objects.get(pk=course_id)
			sidebar = SidebarLinks.objects.filter(sidebar=1).order_by('order')
			faculty = Faculty.objects.get(user=request.user)
			
			if request.method == "POST":			
				form = AddLectureForm(request.POST, request.FILES)
				course1 = Course.objects.get(pk=course_id)
				if form.is_valid():
					new_lecture = form.save(commit=False)
					new_lecture.user = request.user
					new_lecture.course = Course.objects.get(pk=course_id)
					new_lecture.active = True
					new_lecture.save()
					
					alert = EmailAlerts.objects.filter(course=course_id, lecture_alert=True,)
					for student in alert:
						subject = "New Lecture Posted for %s" % (course.short)
						recipients = [student.user.email]
						#recipients = ['pharmacy-faculty@ucwv.edu', 'pharmacy-staff@ucwv.edu']
						sender = 'sopwebmail@ucwv.edu'

						text_content = loader.get_template('fife/alerts_lecture.txt')
						html_content = loader.get_template('fife/alerts_lecture.html')
						c = Context({
							'course': course,
							'new_lecture': new_lecture,
							'student': student,
						})

						msg = EmailMultiAlternatives(subject, text_content.render(c), sender, recipients,)
						msg.attach_alternative(html_content.render(c), "text/html")
						msg.send()
					
					return HttpResponseRedirect('/fife/course/%s/' % course.pk)
			else:
				form = AddLectureForm()

			return render_to_response('fife/faculty_add_lecture.html', {'form': form, 'course': course, 'sidebar': sidebar, 'faculty': faculty}, context_instance=RequestContext(request))
		else:
			return HttpResponseRedirect('/fife/error/')	

	else:
		return HttpResponseRedirect('/mayberry/login/')
		
def lecture_edit(request, lecture_id):
	if request.user.is_authenticated():
		
		if [x for x in request.user.groups.all() if x.pk in [1]]:
		
			lecture = Lecture.objects.get(pk=lecture_id)
			course = Course.objects.get(pk=lecture.course.pk)
			sidebar = SidebarLinks.objects.filter(sidebar=1).order_by('order')
			faculty = Faculty.objects.get(user=request.user)
			
			if request.method == "POST":			
				form = AddLectureForm(request.POST, request.FILES, instance=lecture)
				if form.is_valid():
					form.save()
					
					return HttpResponseRedirect('/fife/course/%s/' % course.pk)
			else:
				form = AddLectureForm(instance=lecture)
			return render_to_response('fife/faculty_edit_lecture.html', {'form': form, 'course': course, 'lecture': lecture, 'sidebar': sidebar, 'faculty': faculty,}, context_instance=RequestContext(request))	
		else:
			return HttpResponseRedirect('/fife/error/')	
		
		
	else:
		return HttpResponseRedirect('/mayberry/login/')
		
def lecture_delete(request, lecture_id):
	lecture = Lecture.objects.get(pk=lecture_id)
	course = Course.objects.get(pk=lecture.course.pk)
	lecture.active = False
	lecture.save()
	
	return HttpResponseRedirect('/fife/course/%s/' % course.pk)

def lecture_remove(request):
	pass
		
def book_add(request, course_id):
	if request.user.is_authenticated():

		if [x for x in request.user.groups.all() if x.pk in [1]]:

			course = Course.objects.get(pk=course_id)
			sidebar = SidebarLinks.objects.filter(sidebar=1).order_by('order')
			faculty = Faculty.objects.get(user=request.user)
			
			if request.method == "POST":			
				form = AddBookForm(request.POST)
				if form.is_valid():
					new_book = form.save(commit=False)
					new_book.course = Course.objects.get(pk=course_id)
					new_book.active = True
					new_book.save()

					return HttpResponseRedirect('/fife/course/%s/' % course.pk)
			else:
				form = AddBookForm()

			return render_to_response('fife/faculty_add_book.html', {'form': form, 'course': course, 'sidebar': sidebar, 'faculty': faculty,}, context_instance=RequestContext(request))

		else:
			return HttpResponseRedirect('/fife/error/')

	else:
		return HttpResponseRedirect('/mayberry/login/')
		
def book_edit(request, book_id):
	if request.user.is_authenticated():

		if [x for x in request.user.groups.all() if x.pk in [1]]:

			book = RequiredBook.objects.get(pk=book_id)
			course = Course.objects.get(pk=book.course.pk)
			sidebar = SidebarLinks.objects.filter(sidebar=1).order_by('order')
			faculty = Faculty.objects.get(user=request.user)
			
			if request.method == "POST":			
				form = AddBookForm(request.POST, instance=book)
				if form.is_valid():
					form.save()

					return HttpResponseRedirect('/fife/course/%s/' % course.pk)
			else:
				form = AddBookForm(instance=book)
					
			return render_to_response('fife/faculty_edit_book.html', {'form': form, 'course': course, 'book': book, 'sidebar': sidebar, 'faculty': faculty,}, context_instance=RequestContext(request))	
		else:
			return HttpResponseRedirect('/fife/error/')	

	else:
		return HttpResponseRedirect('/mayberry/login/')

def faculty_info(request, faculty_id):
	if request.user.is_authenticated():

		if [x for x in request.user.groups.all() if x.pk in [9]]:

			this_faculty = Faculty.objects.get(pk=faculty_id)
			sidebar = SidebarLinks.objects.filter(sidebar=3).order_by('order')
			
			return render_to_response('fife/student_faculty_info.html', {'this_faculty': this_faculty,  'sidebar': sidebar,}, context_instance=RequestContext(request))
		
		elif [x for x in request.user.groups.all() if x.pk in [1]]:
			
			this_faculty = Faculty.objects.get(pk=faculty_id)
			sidebar = SidebarLinks.objects.filter(sidebar=1).order_by('order')
			faculty = Faculty.objects.get(user=request.user)
			
			if this_faculty.user.pk == request.user.pk:
				edit_this = True
			else:
				edit_this = False

			return render_to_response('fife/faculty_faculty_info.html', {'this_faculty': this_faculty, 'faculty': faculty, 'sidebar': sidebar, 'edit': edit_this }, context_instance=RequestContext(request))
			
		else:
			return HttpResponseRedirect('/fife/error/')	

	else:
		return HttpResponseRedirect('/mayberry/login/')
						
def faculty_edit(request, faculty_id):
	if request.user.is_authenticated():

		if [x for x in request.user.groups.all() if x.pk in [1]]:

			faculty = Faculty.objects.get(pk=faculty_id)
			sidebar = SidebarLinks.objects.filter(sidebar=1).order_by('order')
			
			try:
				user = User.objects.get(pk=faculty.user.pk)
				if request.method == "POST":			
					form = FacultyForm(request.POST, instance=faculty)
					if form.is_valid():
						form.save()

						return HttpResponseRedirect('/fife/')
				else:
					form = FacultyForm(instance=faculty)

				return render_to_response('fife/faculty_edit.html', {'faculty': faculty, 'form': form, 'sidebar': sidebar}, context_instance=RequestContext(request))
			
			except User.DoesNotExist:
				return HttpResponseRedirect('/fife/error/')
		else:
			return HttpResponseRedirect('/fife/error/')	

	else:
		return HttpResponseRedirect('/mayberry/login/')
		
def book_delete(request, book_id):
	book = RequiredBook.objects.get(pk=book_id)
	course = Course.objects.get(pk=book.course.pk)
	book.active = False
	book.save()

	return HttpResponseRedirect('/fife/course/%s/' % course.pk)
	
def audio_upload(request):
	if request.user.pk == 1 or request.user.pk == 442 or request.user.pk == 3 or request.user.pk == 1027:
		
		if request.method == "POST":			
			form = AudioForm(request.POST, request.FILES)
			if form.is_valid():
				new_audio = form.save(commit=False)
				new_audio.active = True
				new_audio.save()
				
				course = Course.objects.get(pk=new_audio.course.pk)
				
				alert = EmailAlerts.objects.filter(course=course.pk, audio_alert=True,)
				for student in alert:
					subject = "New Audio Posted for %s" % (course.short)
					recipients = [student.user.email]
					#recipients = ['pharmacy-faculty@ucwv.edu', 'pharmacy-staff@ucwv.edu']
					sender = 'sopwebmail@ucwv.edu'
					
					text_content = loader.get_template('fife/alerts_audio.txt')
					html_content = loader.get_template('fife/alerts_audio.html')
					c = Context({
						'course': course,
						'new_audio': new_audio,
						'student': student,
					})

					msg = EmailMultiAlternatives(subject, text_content.render(c), sender, recipients,)
					msg.attach_alternative(html_content.render(c), "text/html")
					msg.send()

				#return HttpResponseRedirect('/fife/audio/upload/')
				return HttpResponseRedirect('/fife/course/%s/' % course.pk)
		else:
			form = AudioForm()

		return render_to_response('fife/upload_audio.html', {'form': form, }, context_instance=RequestContext(request))

		
	else:
		return HttpResponseRedirect('/fife/error/')

def audio_edit(request, audio_id):
	if request.user.pk == 1 or request.user.pk == 442 or request.user.pk == 3 or request.user.pk == 1027:
	
		audio = Audio.objects.get(pk=audio_id)
	
		if request.method == "POST":			
			form = AudioForm(request.POST, request.FILES, instance=audio)
			if form.is_valid():
				new_audio = form.save(commit=False)
				new_audio.active = True
				new_audio.save()
			
				course = Course.objects.get(pk=new_audio.course.pk)

			#return HttpResponseRedirect('/fife/audio/upload/')
				return HttpResponseRedirect('/fife/course/%s/' % course.pk)
		else:
			form = AudioForm(instance=audio)
			
		return render_to_response('fife/edit_audio.html', {'form': form, 'audio': audio }, context_instance=RequestContext(request))
	
	else:
		return HttpResponseRedirect('/fife/error/')	
		
def audio_delete(request, audio_id):
	audio = Audio.objects.get(pk=audio_id)
	course = Course.objects.get(pk=audio.course.pk)
	audio.active = False
	audio.save()

	return HttpResponseRedirect('/fife/course/%s/' % course.pk)
	
def audio_uploaded(request):
	pass
	
def resources(request):
	if request.user.is_authenticated():
		return render_to_response('fife/resources.html', { }, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/mayberry/login/')
		
def error_page(request):
	if request.user.is_authenticated():
		
		if request.method == "POST":			
			form = ErrorForm(request.POST)
			if form.is_valid():
				first_name = form.cleaned_data['first_name']
				last_name = form.cleaned_data['last_name']
				from_email = form.cleaned_data['email']
				the_message = form.cleaned_data['message']
				

				subject = "Error Reported on Fife by %s %s" % (first_name, last_name)
				recipients = ['chrismccomas@ucwv.edu']
				sender = 'sopwebmail@ucwv.edu'
				message = the_message

				from django.core.mail import send_mail
				send_mail(subject, message, sender, recipients)
				

				return HttpResponseRedirect('/fife/')
		else:
			form = ErrorForm()

		return render_to_response('fife/error_form.html', {'form': form,}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/mayberry/login/')
		
def resource_add(request, course_id):
	if request.user.is_authenticated():

		if [x for x in request.user.groups.all() if x.pk in [1]]:

			course = Course.objects.get(pk=course_id)
			sidebar = SidebarLinks.objects.filter(sidebar=1).order_by('order')
			faculty = Faculty.objects.get(user=request.user)

			if request.method == "POST":			
				form = AddResourceForm(request.POST, request.FILES)
				course1 = Course.objects.get(pk=course_id)
				if form.is_valid():
					new_resource = form.save(commit=False)
					new_resource.user = request.user
					new_resource.course = Course.objects.get(pk=course_id)
					new_resource.active = True
					new_resource.save()

					return HttpResponseRedirect('/fife/course/%s/' % course.pk)
				
			else:
				form = AddResourceForm()

				
			return render_to_response('fife/faculty_add_resource.html', {'form': form, 'course': course, 'sidebar': sidebar, 'faculty': faculty}, context_instance=RequestContext(request))
		
		else:
			return HttpResponseRedirect('/fife/error/')	

	else:
		return HttpResponseRedirect('/mayberry/login/')	
		
def resource_edit(request, resource_id):
	if request.user.is_authenticated():

		if [x for x in request.user.groups.all() if x.pk in [1]]:

			resource = Resource.objects.get(pk=resource_id)
			course = Course.objects.get(pk=resource.course.pk)
			sidebar = SidebarLinks.objects.filter(sidebar=1).order_by('order')
			faculty = Faculty.objects.get(user=request.user)

			if request.method == "POST":			
				form = AddResourceForm(request.POST, request.FILES, instance=resource)
				if form.is_valid():
					form.save()

					return HttpResponseRedirect('/fife/course/%s/' % course.pk)
			else:
				form = AddResourceForm(instance=resource)
					
			return render_to_response('fife/faculty_edit_resource.html', {'form': form, 'course': course, 'resource': resource, 'sidebar': sidebar, 'faculty': faculty,}, context_instance=RequestContext(request))	
		else:
			return HttpResponseRedirect('/fife/error/')	

	else:
		return HttpResponseRedirect('/mayberry/login/')
		
def resource_delete(request, resource_id):
	resource = Resource.objects.get(pk=resource_id)
	course = Course.objects.get(pk=resource.course.pk)
	resource.active = False
	resource.save()

	return HttpResponseRedirect('/fife/course/%s/' % course.pk)
	