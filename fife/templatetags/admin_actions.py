from django import template
from django.contrib.auth.models import User, Group

register = template.Library()

def admin_actions():
	
	if [x for x in request.user.groups.all() if x.pk in [10]]:
		admin = True
	else:
		admin = []
	return {'admin': admin}
        
register.inclusion_tag('chet/admin_actions.html')(admin_actions)