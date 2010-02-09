from django import forms
from fife.courses.models import *
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader, RequestContext
from django.contrib.localflavor.us.forms import USPhoneNumberField, USZipCodeField, USStateField, USStateSelect

class ErrorForm(forms.Form):

	# name info
	first_name = forms.CharField(max_length=100)
	last_name = forms.CharField(max_length=100)
	email = forms.EmailField()
	message = forms.CharField(widget=forms.Textarea)

class CourseForm(forms.ModelForm):
	title = forms.CharField(widget=forms.TextInput(attrs={'size': '60' }), required=False, help_text="Format: PHAR510: Introduction to Pharmacy Practice and Law",)
	short = forms.CharField(widget=forms.TextInput(attrs={'size': '15' }), required=False,  help_text="Format: PHAR510",)
	credit_hours = forms.CharField(widget=forms.TextInput(attrs={'size': '2' }), required=False,)
	class_location = forms.CharField(widget=forms.TextInput(attrs={'size': '5' }), required=False,)
	
	class Meta:
		model = Course
		
class AddCourseForm(forms.ModelForm):
	title = forms.CharField(widget=forms.TextInput(attrs={'size': '60' }), required=False, help_text="Format: PHAR510: Introduction to Pharmacy Practice and Law",)
	short = forms.CharField(widget=forms.TextInput(attrs={'size': '15' }), required=False,  help_text="Format: PHAR510",)
	credit_hours = forms.CharField(widget=forms.TextInput(attrs={'size': '2' }), required=False,)
	class_location = forms.CharField(widget=forms.TextInput(attrs={'size': '5' }), required=False,)
	
	class Meta:
		model = Course
		exclude = ('instructor')
		
class AddBookForm(forms.ModelForm):

	class Meta:
		model = RequiredBook
		exclude = ('course', 'active')
		
class AddLectureForm(forms.ModelForm):
	
	lecture_date = forms.CharField(widget=forms.TextInput(attrs={'class': 'w16em dateformat-Y-ds-m-ds-d' }), required=False)
	
	class Meta:
		model = Lecture
		exclude = ('course', 'user', 'created_date', 'audio', 'active',)
		
class AddAnnouncementForm(forms.ModelForm):
	
	class Meta:
		model = Announcement
		exclude = ('created_date', 'course', 'user', 'active',)
		
class AlertForm(forms.ModelForm):

	class Meta:
		model = EmailAlerts
		exclude = ('course', 'user',)
		
class AudioForm(forms.ModelForm):
	
	audio_date = forms.CharField(widget=forms.TextInput(attrs={'class': 'w16em dateformat-Y-ds-m-ds-d' }), required=False)
	
	class Meta:
		model = Audio
		exclude = ('uploaded_date')
		
class FacultyForm(forms.ModelForm):

	class Meta:
		model = Faculty
		exclude = ('user', 'active')
		
class AddResourceForm(forms.ModelForm):

	class Meta:
		model = Resource
		exclude = ('course', 'user', 'created_date', 'active',)