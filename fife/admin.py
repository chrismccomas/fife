from ucwv.fife.models import *
from django.contrib import admin

class ResourceAdmin(admin.ModelAdmin):
	pass
admin.site.register(Resource, ResourceAdmin)

class EmailAlertsAdmin(admin.ModelAdmin):
	pass
admin.site.register(EmailAlerts, EmailAlertsAdmin)

class SidebarLinksAdmin(admin.ModelAdmin):
	list_display = ('title', 'sidebar', 'order')
admin.site.register(SidebarLinks, SidebarLinksAdmin)

class ClassYearAdmin(admin.ModelAdmin):
	pass
admin.site.register(ClassYear, ClassYearAdmin)

class AnnouncementAdmin(admin.ModelAdmin):
	pass
admin.site.register(Announcement, AnnouncementAdmin)

class TermAdmin(admin.ModelAdmin):
	pass
admin.site.register(Term, TermAdmin)

class FacultyAdmin(admin.ModelAdmin):
	pass
admin.site.register(Faculty, FacultyAdmin)

class CourseAdmin(admin.ModelAdmin):
	list_display = ('title', 'term',)
admin.site.register(Course, CourseAdmin)

class RequiredBookAdmin(admin.ModelAdmin):
	pass
admin.site.register(RequiredBook, RequiredBookAdmin)

class LectureAdmin(admin.ModelAdmin):
	list_display = ('title', 'speaker', 'user')
admin.site.register(Lecture, LectureAdmin)

class AudioAdmin(admin.ModelAdmin):
	pass
admin.site.register(Audio, AudioAdmin)