from datetime import datetime
from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.localflavor.us.models import PhoneNumberField
#from django.contrib.sites.models import Site

"""
'FIFE'
University of Charleston School of Pharmacy Course Management Application
Developed by Christopher McComas
Version: 0.1
Date: 04-20-2009
"""

FACULTY_STATUS = 1
STAFF_STATUS = 2
STUDENT_STATUS = 3
USER_CHOICES = (
	(FACULTY_STATUS, 'Faculty'),
	(STAFF_STATUS, 'Staff'),
	(STUDENT_STATUS, 'Student'),
)
	
class SidebarLinks(models.Model):
	"""
	This model is for the links on the left side of each page.
	"""
	title = models.CharField(max_length=250,)
	url = models.CharField(max_length=500,)
	sidebar = models.IntegerField(choices=USER_CHOICES, default=FACULTY_STATUS,)
	order = models.IntegerField()
	
	class Meta:
		verbose_name_plural = 'Sidebar Links'
		ordering = ('sidebar', 'order')
		
	def __unicode__(self):
		return '%s' % (self.title)
		
class ClassYearLive(models.Manager):
	"""
	Get only the Class Years that are currently set to active
	"""
	def get_query_set(self):
		return super(ClassYearLive,
				self).get_query_set().filter(active=1)
					
class ClassYear(models.Model):
	"""
	This model is for the class years, example: Class of 2010, 2011, etc
	The group field is a foreign key link to django.groups that match the class list to easily assign students to their class year
	"""
	title = models.CharField(max_length=250,)
	group = models.ForeignKey(Group, unique=True)
	active = models.BooleanField()
	
	objects = models.Manager()
	year_live = ClassYearLive()
	
	def __unicode__(self):
		return '%s' % (self.title)
	
class TermLive(models.Manager):
	"""
	Get only the Terms that are currently set to active
	"""
	def get_query_set(self):
		return super(TermLive,
				self).get_query_set().filter(active=1)
				
class Term(models.Model):
	"""
	This model is for the school term, example: Fall 2009, Spring 2010, etc.
	"""
	short = models.CharField("Short Title", max_length=4, help_text="Format: F09",)
	year = models.CharField(max_length=4,)
	title = models.CharField("Full Title", max_length=100, help_text="Format: Fall 2009",)	
	active = models.BooleanField()
	
	objects = models.Manager()
	term_live = TermLive()
	
	def __unicode__(self):
		return '%s' % (self.title)

class FacultyLive(models.Manager):
	"""
	Get only the Faculty Members that are currently set to active
	"""
	def get_query_set(self):
		return super(FacultyLive,
				self).get_query_set().filter(active=1)
				
class Faculty(models.Model):
	"""
	This model is for the faculty members, teaching courses at UCSOP.
	The user field is a foreign key link to django.users that match the faculty member to draw their information including name, email address, etc
	"""
	user = models.ForeignKey(User, unique=True, limit_choices_to={'groups': 1})
	office_hours = models.CharField(max_length=25, blank=True,)
	office_location =  models.CharField(max_length=25, blank=True,)
	active = models.BooleanField()
	phone_number = PhoneNumberField('Office Phone', blank=True,)
	
	objects = models.Manager()
	faculty_live = FacultyLive()
	
	class Meta:
		verbose_name = 'Faculty Member'
		verbose_name_plural = 'Faculty Members'
	
	def __unicode__(self):
		return '%s %s' % (self.user.first_name, self.user.last_name)
			
class CourseLive(models.Manager):
	"""
	Get only the Courses that are currently set to active
	"""
	def get_query_set(self):
		return super(CourseLive,
				self).get_query_set().filter(active=1)
							
class Course(models.Model):
	"""
	This model is for the faculty members, teaching courses at UCSOP.
	The term field is a foreign key link to the Term model, only getting those Terms that are set to active
	The instructor field is a foreign key link to the Faculty model, only getting those Faculty Members that are set to active
	The classyear field is a foreign key link to the ClassYear model, only getting those class years that are set to active
	"""
	title = models.CharField("Full Title", max_length=250, help_text="Format: PHAR510: Introduction to Pharmacy Practice and Law",)
	short = models.CharField("Short Title", max_length=10, help_text="Format: PHAR510",)
	instructor = models.ManyToManyField(Faculty, related_name='course_instructor', limit_choices_to={'active': True}, blank=True,)
	course_description = models.TextField(blank=True,)
	credit_hours = models.CharField(max_length=3, blank=True,)
	class_schedule = models.CharField(max_length=250, blank=True,)
	class_location = models.CharField(max_length=250, blank=True,)
	syllabus = models.FileField(upload_to='fife/syllabus', blank=True, null=True,)
	
	term = models.ForeignKey(Term,)
	classyear = models.ForeignKey(ClassYear, limit_choices_to={'active': True})
	
	objects = models.Manager()
	course_live = CourseLive()
	
	course_coordinator = models.ManyToManyField(Faculty, related_name='course_coordinator', limit_choices_to={'active': True}, blank=True,)
	
	class Meta:
		ordering = ['title']
	
	def get_absolute_url(self):
		return "/fife/course/%i/" % self.id
	
	def __unicode__(self):
		return '%s %s' % (self.term, self.short)

class RequiredBookLive(models.Manager):
	"""
	Get only the RequiredBook that are currently set to active
	"""
	def get_query_set(self):
		return super(RequiredBookLive,
			self).get_query_set().filter(active=1)
							
class RequiredBook(models.Model):
	"""
	This model is for the Required Books for each course.
	The course field is a foreign key link to the Course model, only getting those Courses that are set to active
	"""
	title = models.CharField(max_length=250,)
	description = models.TextField(blank=True,)
	link = models.URLField(verify_exists=False, blank=True,)
	course = models.ForeignKey(Course, limit_choices_to={'term__active': True})
	active = models.BooleanField(default=True,)
	
	objects = models.Manager()
	book_live = RequiredBookLive()
	
	def __unicode__(self):
		return '%s' % (self.title)	

class AnnouncementLive(models.Manager):
	"""
	Get only the Announcement that are currently set to active
	"""
	def get_query_set(self):
		return super(AnnouncementLive,
			self).get_query_set().filter(active=1)
					
class Announcement(models.Model):
	"""
	This model is for the class Announcements for each course.
	The course field is a foreign key link to the Course model, only getting those Courses that are set to active
	"""
	created_date = models.DateTimeField(auto_now=True,)
	course = models.ForeignKey(Course, limit_choices_to={'term__active': True})
	user = models.ForeignKey(User, limit_choices_to={'groups': 1})
	title = models.CharField(max_length=250,)
	message = models.TextField()
	email = models.BooleanField()
	active = models.BooleanField(default=True,)
	
	objects = models.Manager()
	announcement_live = AnnouncementLive()
	
	def __unicode__(self):
		return "%s - %s" % (self.course.short, self.title)
		
	def get_absolute_url(self):
		return "/fife/announcements/%i/" % self.id

class LectureLive(models.Manager):
	"""
	Get only the Lectures that are currently set to active
	"""
	def get_query_set(self):
		return super(LectureLive,
			self).get_query_set().filter(active=1)	
			
class Lecture(models.Model):
	"""
	This model is for the class Lectures for each course.
	The course field is a foreign key link to the Course model, only getting those Courses that are set to active
	"""
	created_date = models.DateTimeField(auto_now=True,)
	course = models.ForeignKey(Course, limit_choices_to={'term__active': True})
	title = models.CharField("Title of Lecture", max_length=250,)
	lecture_date = models.DateField("Date of Lecture",)
	speaker = models.CharField(max_length=250, blank=True, help_text="Only enter if speaker is a non UCSOP faculty member",)
	powerpoint = models.FileField("File", upload_to='fife/lectures', blank=True, null=True,)
	user = models.ForeignKey(User,)
	active = models.BooleanField(default=True,)
	
	objects = models.Manager()
	lecture_live = LectureLive()
	
	def __unicode__(self):
		return '%s %s' % (self.course, self.lecture_date)
		
	def get_absolute_url(self):
		return "/fife/lectures/%i/" % self.id

class AudioLive(models.Manager):
	"""
	Get only the Audio that are currently set to active
	"""
	def get_query_set(self):
		return super(AudioLive,
			self).get_query_set().filter(active=1)
							
class Audio(models.Model):
	"""
	This model is for the class Audio for each course.
	The course field is a foreign key link to the Course model, only getting those Courses that are set to active
	"""
	uploaded_date = models.DateTimeField(auto_now=True,)
	course = models.ForeignKey(Course, limit_choices_to={'term__active': True})
	audio_date = models.DateField("Date of Lecture",)
	audio = models.FileField(upload_to='fife/lectures/audio', blank=True, null=True,)
	active = models.BooleanField(default=True,)
	
	objects = models.Manager()
	audio_live = AudioLive()

	def __unicode__(self):
		return '%s %s' % (self.course, self.audio_date)
		
class EmailAlerts(models.Model):
	user = models.ForeignKey(User,)
	course = models.ForeignKey(Course,)
	announcement_alert = models.BooleanField(default=True,)
	audio_alert = models.BooleanField(default=True,)
	lecture_alert = models.BooleanField(default=True,)
	
	class Meta:
		verbose_name = 'Email Alert'
		verbose_name_plural = 'Email Alerts'
	
	def __unicode__(self):
		return 'Alerts for %s %s %s' % (self.course.short, self.user.first_name, self.user.last_name)
		
class ResourceLive(models.Manager):
	"""
	Get only the Lectures that are currently set to active
	"""
	def get_query_set(self):
		return super(ResourceLive,
			self).get_query_set().filter(active=1)	

class Resource(models.Model):
	"""
	This model is for the class Resources for each course.
	The course field is a foreign key link to the Course model, only getting those Courses that are set to active
	"""
	created_date = models.DateTimeField(auto_now=True,)
	course = models.ForeignKey(Course, limit_choices_to={'term__active': True})
	title = models.CharField("Title of Resource", max_length=250,)
	document = models.FileField("File", upload_to='fife/resources', blank=True, null=True,)
	user = models.ForeignKey(User,)
	active = models.BooleanField(default=True,)

	objects = models.Manager()
	resource_live = ResourceLive()

	def __unicode__(self):
		return '%s %s' % (self.course, self.created_date)

	def get_absolute_url(self):
		return "/fife/resources/%i/" % self.id