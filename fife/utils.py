from django.conf import settings
import datetime
from decimal import Decimal
from django.contrib.auth.models import User, Group
from ucwv.supapp.models import *
from ucwv.students.models import *
from ucwv.fife.models import *
from ucwv.openhouse.models import *
from django.template import loader, Context
from django.core.mail import EmailMultiAlternatives

def fife():
	course = Course.objects.get(pk=15)
	print course.instructor.all()
	
def totals():
	
	app = CognitiveAbility.objects.all()
	
	for entry in app:
		try:
			total = CogTotals.objects.get(cog_ability=entry.pk)
			#print "User already exists for %s %s" % (entry.first_name, entry.last_name)
		except CogTotals.DoesNotExist:
			
			if entry.gpa_math_weight:
				gpa_math = Decimal(entry.gpa_math_weight)
			else:
				gpa_math = 0
				
			if entry.gpa_science_weight:
				gpa_science = Decimal(entry.gpa_science_weight)
			else:
				gpa_science = 0
				
			if entry.gpa_socsci_weight:
				gpa_socsci = Decimal(entry.gpa_socsci_weight)
			else:
				gpa_socsci = 0
				
			if entry.pcat_comp_weight:
				pcat_comp = Decimal(entry.pcat_comp_weight)
			else:
				pcat_comp = 0
				
			if entry.pcat_essay_weight:
				pcat_essay = Decimal(entry.pcat_essay_weight)
			else:
				pcat_essay = 0
				
			if entry.letter_rec_1:
				letter_1 = Decimal(entry.letter_rec_1)
			else:
				letter_1 = 0	
				
			if entry.letter_rec_2:
				letter_2 = Decimal(entry.letter_rec_2)
			else:
				letter_2 = 0
				
			if entry.comm_service_score:
				comm_service = Decimal(entry.comm_service_score)
			else:
				comm_service = 0
				
			if entry.interview_score_weight:
				interview = Decimal(entry.interview_score_weight)
			else:
				interview = 0
				
			if entry.add_uc:
				add_uc = Decimal(entry.add_uc)
			else:
				add_uc = 0
			
			if entry.add_ug_degree:
				add_ug_degree = Decimal(entry.add_ug_degree)
			else:
				add_ug_degree = 0
				
			if entry.add_pharm_exp:
				add_pharm_exp = Decimal(entry.add_pharm_exp)
			else:
				add_pharm_exp = 0
				
			if entry.add_appl_resident:
				add_appl_resident = Decimal(entry.add_appl_resident)
			else:
				add_appl_resident = 0
				
			if entry.add_rural_resident:
				add_rural_resident = Decimal(entry.add_rural_resident)
			else:
				add_rural_resident = 0
				
			totals = CogTotals()
			totals.cog_ability = CognitiveAbility.objects.get(pk=entry.pk)
			totals.sec1_total = gpa_math + gpa_science + gpa_socsci + pcat_comp + pcat_essay
			totals.sec2_total = letter_1 + letter_2 +comm_service + interview
			totals.sec3_total = add_uc + add_ug_degree + add_pharm_exp + add_appl_resident + add_rural_resident
			totals.grand_total = totals.sec1_total + totals.sec2_total + totals.sec3_total
			totals.save()
	
def addition_reset():
	
	app = CognitiveAbility.objects.all()
	
	for entry in app:
		if entry.subcmte_mtg4_date:
			entry.subcmte_mtg4_date = []
			entry.save()
		else:
			pass
		
def outstanding():
	
	today = "2009-05-21"
	status = AdmitContact.objects.all().order_by('last_name', 'first_name')
	
	for entry in status:
		if entry.deposit_1_amount:
			pass
		else:
			if str(entry.tuition_deadline) < today:
				pass
			else:
				if entry.official_sent:
					if entry.declined_offer:
						pass
					else:
						print "%s, %s" % (entry.last_name, entry.first_name)
				
	
	
def packet_total():
	
	app = CognitiveAbility.objects.filter(subcmte_mtg2__isnull=False)
		
	for entry in app:
			
			if entry.gpa_math_weight:
				gpa_math = Decimal(entry.gpa_math_weight)
			else:
				gpa_math = 0
				
			if entry.gpa_science_weight:
				gpa_science = Decimal(entry.gpa_science_weight)
			else:
				gpa_science = 0
				
			if entry.gpa_socsci_weight:
				gpa_socsci = Decimal(entry.gpa_socsci_weight)
			else:
				gpa_socsci = 0
				
			if entry.pcat_comp_weight:
				pcat_comp = Decimal(entry.pcat_comp_weight)
			else:
				pcat_comp = 0
				
			if entry.pcat_essay_weight:
				pcat_essay = Decimal(entry.pcat_essay_weight)
			else:
				pcat_essay = 0
				
			if entry.letter_rec_1:
				letter_1 = Decimal(entry.letter_rec_1)
			else:
				letter_1 = 0	
				
			if entry.letter_rec_2:
				letter_2 = Decimal(entry.letter_rec_2)
			else:
				letter_2 = 0
				
			if entry.comm_service_score:
				comm_service = Decimal(entry.comm_service_score)
			else:
				comm_service = 0
				
			if entry.interview_score_weight:
				interview = Decimal(entry.interview_score_weight)
			else:
				interview = 0
				
			if entry.add_uc:
				add_uc = Decimal(entry.add_uc)
			else:
				add_uc = 0
			
			if entry.add_ug_degree:
				add_ug_degree = Decimal(entry.add_ug_degree)
			else:
				add_ug_degree = 0
				
			if entry.add_pharm_exp:
				add_pharm_exp = Decimal(entry.add_pharm_exp)
			else:
				add_pharm_exp = 0
				
			if entry.add_appl_resident:
				add_appl_resident = Decimal(entry.add_appl_resident)
			else:
				add_appl_resident = 0
				
			if entry.add_rural_resident:
				add_rural_resident = Decimal(entry.add_rural_resident)
			else:
				add_rural_resident = 0
				
		
			sec1_total = gpa_math + gpa_science + gpa_socsci + pcat_comp + pcat_essay
			sec2_total = letter_1 + letter_2 +comm_service + interview
			sec3_total = add_uc + add_ug_degree + add_pharm_exp + add_appl_resident + add_rural_resident
			grand_total = sec1_total + sec2_total + sec3_total
			
			if grand_total >= 100:
				print "FAIL: %s %s = %s" % (entry.first_name, entry.last_name, grand_total)
			else:
				pass
			
def students():
	create_user = ContactInformation.objects.all()
	
	for entry in create_user:
		try:
			user = User.objects.get(email=entry.uc_email)
			print "User already exists for %s %s" % (entry.first_name, entry.last_name)
		except User.DoesNotExist:
			new_username = entry.first_name + entry.last_name
			new_username = new_username.lower()
			
			string = ''
			for i in range(6):
				string += random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
			
			user = User.objects.create_user(new_username, entry.uc_email, string)
			user.first_name = entry.first_name
			user.last_name = entry.last_name
			
			if entry.student_class == "Class of 2010":
				user.groups.add(5, 9)
			elif entry.student_class == "Class of 2011":
				user.groups.add(4, 9)
			else:
				user.groups.add(3, 9)

			user.save()
			
			subject = "Your login for the new UCSOP Student Information site"
			recipients = [entry.uc_email]
			#recipients = ['pharmacy-faculty@ucwv.edu', 'pharmacy-staff@ucwv.edu']
			sender = 'sopwebmail@ucwv.edu'
									
			text_content = loader.get_template('students/new_email.txt')
			html_content = loader.get_template('students/new_email.html')
			c = Context({
				'username': new_username,
				'password': string
			})
									
			msg = EmailMultiAlternatives(subject, text_content.render(c), sender, recipients,)
			msg.attach_alternative(html_content.render(c), "text/html")
			msg.send()
			
			entry.user = User.objects.get(email=entry.uc_email)
			entry.save()
			
			try:
				emergency = EmergencyInformation.objects.get(uc_email=entry.uc_email)
				emergency.user = User.objects.get(email=entry.uc_email)
				emergency.save()
			except EmergencyInformation.DoesNotExist:
				pass
		
def students_emergency():
	emergency = EmergencyInformation.objects.filter(user__isnull=True)
	
	for entry in emergency:
		try:
			entry.user = User.objects.get(email=entry.uc_email)
			entry.save()
		except User.DoesNotExist:
			pass
			
def email_addy():
	admit = AdmitContact.objects.filter(deposit_1_amount__gte=500, deposit_withdrew=False)
	for entry in admit:
		print "%s; " % entry.application.user.email

def class_email():
	admit = AdmitContact.objects.filter(deposit_1_amount__gte=500, deposit_withdrew=False)
	withdrew = AdmitContact.objects.filter(deposit_withdrew=True)
	datatel = AdmitContact.objects.filter(deposit_1_amount__gte=500, deposit_withdrew=False).order_by('-official_sent')
	
	total = admit.count()
	total_withdrew = withdrew.count()
	
	subject = "Introducing the UCSOP Class of 2013"
	dt_subject = "DATATEL: Introducing the UCSOP Class of 2013"
	recipients = ['chrismccomas@ucwv.edu', 'nicoleperkins@ucwv.edu']
	#recipients = ['chrismccomas@ucwv.edu']
	sender = 'sopwebmail@ucwv.edu'
	
	import datetime
	from django.conf import settings
	
	cur_time = datetime.datetime.now()
	if cur_time.hour < 12:
		time = 'Morning'
	else:
		time = 'Afternoon'
		
	if cur_time.hour < 12:
		time_2 = 'morning'
	else:
		time_2 = 'afternoon'
							
	text_content = loader.get_template('supapp/class_list.txt')
	html_content = loader.get_template('supapp/class_list.html')
	c = Context({
		'total': total,
		'datatel': datatel,
		'admit': admit,
		'withdrew': withdrew,
		'time': time,
		'time_2': time_2,
	})
	
	dt_text_content = loader.get_template('supapp/class_list.txt')
	dt_html_content = loader.get_template('supapp/class_list_dt.html')
	dt_c = Context({
		'total': total,
		'datatel': datatel,
		'admit': admit,
		'withdrew': withdrew,
		'time': time,
		'time_2': time_2,
	})
							
	msg = EmailMultiAlternatives(subject, text_content.render(c), sender, recipients,)
	msg.attach_alternative(html_content.render(c), "text/html")
	msg.send()
	
	msg = EmailMultiAlternatives(dt_subject, dt_text_content.render(c), sender, recipients,)
	msg.attach_alternative(dt_html_content.render(c), "text/html")
	msg.send()
	
	print "Total Admitted: %s" % (total)
	print "Total Withdrew: %s" % (total_withdrew)

	
def admit_fix():
	admit = AdmitContact.objects.all()
	for entry in admit:
		entry.tuition_receieved = False
		entry.deadline_passed = False
		entry.save()
		
def lor_fix():
	lor = Recommendation.objects.all()
	for entry in lor:
		if entry.rating_adaptability == 2:
			adapt = 10
		else:
			adapt = entry.rating_adaptability 
			
		if entry.rating_communication_oral == 2:
			oral = 10
		else:
			oral = entry.rating_communication_oral 
			
		if entry.rating_communication_written == 2:
			written = 10
		else:
			written = entry.rating_communication_written
			
		if entry.rating_empathy == 2:
			empathy = 10
		else:
			empathy = entry.rating_empathy
			
		if entry.rating_ethics == 2:
			ethics = 10
		else:
			ethics = entry.rating_ethics
			
		if entry.rating_intellectual == 2:
			intellectual = 10
		else:
			intellectual = entry.rating_intellectual
			
		if entry.rating_interpersonal == 2:
			interpersonal = 10
		else:
			interpersonal = entry.rating_interpersonal
			
		if entry.rating_judgement == 2:
			judgement = 10
		else:
			judgement = entry.rating_judgement
			
		if entry.rating_leadership == 2:
			leadership = 10
		else:
			leadership = entry.rating_leadership
			
		if entry.rating_maturity == 2:
			maturity = 10
		else:
			maturity = entry.rating_maturity
			
		if entry.rating_motivation == 2:
			motivation = 10
		else:
			motivation = entry.rating_motivation
			
		if entry.rating_appearance == 2:
			appearance = 10
		else:
			appearance = entry.rating_appearance
			
		if entry.rating_reliability == 2:
			reliability = 10
		else:
			reliability = entry.rating_reliability
			
		entry.rating_adaptability = adapt
		entry.rating_communication_oral = oral
		entry.rating_communication_written = written
		entry.rating_empathy = empathy
		entry.rating_ethics = ethics
		entry.rating_intellectual = intellectual
		entry.rating_interpersonal = interpersonal
		entry.rating_judgement = judgement
		entry.rating_leadership = leadership
		entry.rating_maturity = maturity
		entry.rating_motivation = motivation
		entry.rating_appearance = appearance
		entry.rating_reliability = reliability
		entry.save()
		
def cmte_awards():
	status = ApplicationStatus.objects.all()
	for entry in status:
		if entry.interview_date:
			try:
				app = Application.objects.get(pk=entry.application.pk)
				awards = AwardsAccess()
				awards.application = Application.objects.get(pk=entry.application.pk)
				awards.save()			
			except Application.DoesNotExist:
				pass	
		else:
			pass
			
def cmte_awards1():
	awards = Awards.objects.all()
	for award in awards:
		try:
			access = AwardsAccess.objects.get(application=award.application.pk)
			
			if access.award_title1:
				pass
			else:
				access.award_title1 = award.award_title
				access.award_date1 = award.award_date
				access.award_basis1 = award.award_basis
				access.save()
			
		except AwardsAccess.DoesNotExist:
			pass
		
	
def interviews():
	status = ApplicationStatus.objects.filter(interview_date__isnull=False,)
	for entry in status:
		if entry.interview_date:
			try:
				cog = CognitiveAbility.objects.get(application=entry.app.pk)
			except CognitiveAbility.DoesNotExist:
				print "%s %s" % (entry.first_name, entry.last_name)
		else:
			pass		
	
def cog_ability():
	status = ApplicationStatus.objects.filter(interview_date__isnull=False,).order_by('last_name', 'first_name')
	for entry in status:
		try:
			app = Application.objects.get(pk=entry.app.pk)
			try:
				exist = CognitiveAbility.objects.get(application=entry.app.pk)
				print "Cog Ability Already Exists: %s %s" % (entry.first_name, entry.last_name)
			except CognitiveAbility.DoesNotExist:
				try:
					user = User.objects.get(pk=app.user.pk)
					
					cog = CognitiveAbility()
					cog.application = Application.objects.get(pk=entry.app.pk)
					cog.pharmcas_id = app.pharmcas_id
					cog.email = user.email
					cog.last_name = app.last_name
					cog.first_name = app.first_name
					cog.initials = app.first_name[0] + app.last_name[0]
					cog.social = app.social
					cog.birthdate = app.birth_date
					cog.interview_date = entry.interview_date
					cog.save()		
						
				except User.DoesNotExist:
					print "User Error: %s: %s %s" % (entry.app.pk, entry.first_name, entry.last_name)
		except Application.DoesNotExist:
			print "Application Error: %s: %s %s" % (entry.app.pk, entry.first_name, entry.last_name)

def admit_notify():
	status = ApplicationStatus.objects.filter(interview_date__isnull=False,).order_by('last_name', 'first_name')
	for entry in status:
		try:
			app = Application.objects.get(pk=entry.app.pk)
			try:
				exist = AdmitContact.objects.get(application=entry.app.pk)
				print "Admit Contact Already Exists: %s %s" % (entry.first_name, entry.last_name)
			except AdmitContact.DoesNotExist:
				try:
					user = User.objects.get(pk=app.user.pk)
					
					cog = AdmitContact()
					cog.application = Application.objects.get(pk=entry.app.pk)
					cog.last_name = app.last_name
					cog.first_name = app.first_name
					cog.save()		
						
				except User.DoesNotExist:
					print "User Error: %s: %s %s" % (entry.app.pk, entry.first_name, entry.last_name)
		except Application.DoesNotExist:
			print "Application Error: %s: %s %s" % (entry.app.pk, entry.first_name, entry.last_name)
						
def cog_delete():
	cog = CognitiveAbility.objects.all()
	for entry in cog:
		entry.delete()
	
def submitted_unpaid():
	app = ApplicationStatus.objects.filter(submitted=True, date_deposited__isnull=False,)
	total = app.count()
	print total
	
def address():
	app = Application.objects.filter(curr_dayphone__contains='404')
	for entry in app:
		print "%s %s" % (entry.first_name, entry.last_name)
		
def not_submitted():
	app = Application.objects.filter(submitted=False)
	for entry in app:
		status = ApplicationStatus.objects.get(application=entry.pk)
		if status.initial_status == 4:
			pass
		else:			
			try:
				user = User.objects.get(pk=entry.user)
				app_email = user.email
				app_un = user.username
				app_fn = app.first_name
				app_ln = app.last_name				
				
				subject = "UC Supplemental Application Update"
				recipients = [app_email]
				sender = 'sopwebmail@ucwv.edu'
							
				text_content = loader.get_template('supapp/app_reminder.txt')
				html_content = loader.get_template('supapp/app_reminder.html')
				c = Context({
					'app_fn': app_fn,
					'app_ln': app_ln,
					'app_un': app_un,
					'app_email': app_email
				})
							
				msg = EmailMultiAlternatives(subject, text_content.render(c), sender, recipients)
				msg.attach_alternative(html_content.render(c), "text/html")
				msg.send()
			except User.DoesNotExist:
				pass
			
def status_new():
	status = ApplicationStatus.objects.all()
	for entry in status:
		entry.app = Application.objects.get(pk=entry.application.pk)
		entry.save()
		
		
def lor_review():
	lor = Recommendation.objects.all()
	for entry in lor:
		if entry.right_to_review:
			pass
		else:
			entry.right_to_review = 'I waive my right to review the letter of recommendation'
			entry.save()
	
def lor_date():
	lor = Recommendation.objects.filter(submitted=1, recommend_date__isnull=True)
	for entry in lor:
		print "%s %s / %s %s" % (entry.first_name, entry.last_name, entry.recommender_first_name, entry.recommender_last_name)

def brandi():
	app = ApplicationStatus.objects.filter(submitted=1)
	for entry in app:
		if entry.date_letter1 or entry.date_letter2 or entry.date_letter3 or entry.date_letter4 or entry.date_letter5 or entry.date_letter6:
			pass
		else:
			print "%s %s" % (entry.first_name, entry.last_name)
			
def datetest():
	date = '2008-12-19'
	format = date.strftime(F)
	print format
	
def groups(user):
	user = User.objects.get(pk=user)
	groups = Group.objects.filter(user=user)
	for entry in groups:
		print entry.pk
	
def pharmcas():
	date = '2008-12-05'
	status = ApplicationStatus.objects.filter(submitted=1, submitted_date__gte=date)
	for entry in status:
		if entry.access:
			pass
		else:
			app = Application.objects.get(pk=entry.application.pk)
			entry.access = app.pharmcas_id
			entry.save()
			print "%s %s" % (app.first_name, app.last_name)
		
def dates():
	app = Application.objects.filter(submitted=1)
	for entry in app:
		print entry.submitted_date
		
def na():
	app = Application.objects.all()
	for entry in app:
		if entry.maiden_name == 'NA' or entry.maiden_name == 'N/A':
			entry.maiden_name = ''
			entry.save()
		if entry.middle_name == 'NA' or entry.middle_name == 'N/A':
			entry.middle_name = ''
			entry.save()
		
		
def remindertest():
	app = Application.objects.get(pk=221)			
	email = User.objects.get(pk=app.user.pk)
	email_addy = email.email
	app_fn = app.first_name
	app_ln = app.last_name	
	app_un = email.username
	
	from django.core.mail import EmailMultiAlternatives

	subject = "UC Supplemental Application Update"
	recipients = ['christophermccomas@cc.ucwv.edu']
	sender = 'sopwebmail@ucwv.edu'
				
	text_content = loader.get_template('supapp/app_reminder.txt')
	html_content = loader.get_template('supapp/app_reminder.html')
	c = Context({
		'app_fn': app_fn,
		'app_ln': app_ln,
		'app_un': app_un,
		'app_email': email_addy
	})
				
	msg = EmailMultiAlternatives(subject, text_content.render(c), sender, recipients)
	msg.attach_alternative(html_content.render(c), "text/html")
	msg.send()
	
def reminder():
	user = UserSetup.objects.all()
	for entry in user:
		try:
			app = Application.objects.get(user=entry.new_pk)
			if app.submitted == 0:	
				email = User.objects.get(pk=app.user.pk)
				email_addy = email.email
				app_fn = app.first_name
				app_ln = app.last_name	
				app_un = email.username
				
				from django.core.mail import EmailMultiAlternatives

				subject = "UC Supplemental Application Update"
				recipients = [email_addy]
				sender = 'sopwebmail@ucwv.edu'
				
				text_content = loader.get_template('supapp/app_reminder.txt')
				html_content = loader.get_template('supapp/app_reminder.html')
				c = Context({
					'app_fn': app_fn,
					'app_ln': app_ln,
					'app_un': app_un,
					'app_email': email_addy
				})
				
				msg = EmailMultiAlternatives(subject, t.render(c), sender, recipients)
				msg.attach_alternative(html_content, "text/html")
				msg.send()
			
				print "%s %s %s" % (app.first_name, app.last_name, email.email)
			else:
				pass
		except Application.DoesNotExist:
			pass
			
def new_app():
	convert = AppConvert.objects.filter(user__isnull=False)
	for entry in convert:
		try:
			app = Application.objects.get(user=entry.user)						
		except Application.DoesNotExist:
			newapp = Application()
			newapp.user = entry.user
			newapp.application_year = ApplicationYear.objects.get(active=1)
			newapp.update_date = '2008-12-10'
			newapp.created_date = '2008-12-10'
			newapp.submitted = 0
			newapp.social = entry.social
			newapp.pharmcas_id = entry.pharmcas_id
			newapp.first_name = entry.first_name
			newapp.last_name = entry.last_name
			newapp.middle_name = entry.middle_name
			newapp.maiden_name = entry.maiden_name
			newapp.nickname = entry.nickname
			newapp.gender = entry.gender
			newapp.birth_date = entry.birth_date
			newapp.ethnicity = entry.ethnicity
			newapp.curr_street = entry.curr_street
			newapp.curr_city = entry.curr_city
			newapp.curr_state = entry.curr_state
			newapp.curr_nonus = entry.curr_nonus
			newapp.curr_zip = entry.curr_zip
			newapp.curr_dayphone = entry.curr_dayphone
			newapp.curr_eveningphone = entry.curr_eveningphone
			newapp.curr_mobilephone = entry.curr_mobilephone
			newapp.perm_same = 0
			newapp.perm_street = entry.perm_street
			newapp.perm_city = entry.perm_city
			newapp.perm_state = entry.perm_state
			newapp.perm_nonus = entry.perm_nonus
			newapp.perm_zip = entry.perm_zip
			newapp.birth_city = entry.birth_city
			newapp.birth_state = entry.birth_state
			newapp.birth_nonus = entry.birth_nonus
			newapp.birth_country = entry.birth_country
			newapp.hometown_city = entry.hometown_city
			newapp.hometown_state = entry.hometown_state
			newapp.hometown_nonus = entry.hometown_nonus
			newapp.hometown_country = entry.hometown_country
			newapp.county_citizenship = entry.county_citizenship
			newapp.visa_type = entry.visa_type
			newapp.language_english = entry.language_english
			newapp.toefl = entry.toefl
			newapp.prev_uc = entry.prev_uc
			newapp.prev_pharmacy = entry.prev_pharmacy
			newapp.prev_pharmacy_school = entry.prev_pharmacy_school
			newapp.prev_eligible = entry.prev_eligible
			newapp.felony_convicted = entry.felony_convicted
			newapp.felony_explanation = entry.felony_explanation
			newapp.save()
			print "%s %s App" % (entry.first_name, entry.last_name)
			
	
def educlean():
	edu = Education.objects.filter(application__isnull=False)
	for entry in edu:
		try:
			app = Application.objects.get(pk=entry.application.pk)
			try:
				edu_dup = Education.objects.get(application=app.pk, school_type=entry.school_type, school=entry.school)
				print "%s: %s = %s" % (entry.application, entry.school, edu_dup.school)
			except Education.DoesNotExist:
				pass
		except Application.DoesNotExist:
			pass
	
			
def lor_submit():
	lor_sub = Recommendation.objects.filter(recommend_date__isnull=True)
	for entry in lor_sub:
		entry.submitted = 0
		entry.save()

def emailbomb():
	x = 0
	while x < 50:
		x += 1
		subject = "Guess what Sam?"
		recipients = ['sammyers@ucwv.edu']
		sender = 'sopwebmail@ucwv.edu'
		message = "You're good looking! I like cheese!"
			 
		from django.core.mail import send_mail
		send_mail(subject, message, sender, recipients)

def ninesocial():
	status = ApplicationStatus.objects.filter(pk__gte=187)
	for entry in status:
		app = Application.objects.get(pk=entry.application.pk)
		entry.social = app.social
		entry.save()
		
def statusnine():
	app = Application.objects.all()
	for entry in app:
		try:
			app = ApplicationStatus.objects.get(application=entry.pk)
		except ApplicationStatus.DoesNotExist:
			newstatus = ApplicationStatus()
			newstatus.application = Application.objects.get(pk=entry.pk)
			newstatus.first_name = entry.first_name
			newstatus.last_name = entry.last_name
			newstatus.social = entry.social
			newstatus.initial_status = 3
			newstatus.save()
			print "%s %s" % (entry.first_name, entry.last_name)
			

def ninth():
	app = Application.objects.filter(pk__gt=299)
	for entry in app:
		try:
			user = User.objects.get(pk=entry.pk)
			string = ''
			for i in range(6):
				string += random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
		
			user.set_password(string)
			user.save()
			email = user.email
			app_fn = user.first_name
			app_ln = user.last_name	
			app_un = user.username
			t = loader.get_template('supapp/app_newemail.html')
			c = Context({
				'app_fn': app_fn,
				'app_ln': app_ln,
				'app_un': app_un,
				'app_pw': string,
			})
										
			subject = "UC Supplemental Application Update"
			recipients = [email]
			sender = 'sopwebmail@ucwv.edu'
				#message = 
								 
			from django.core.mail import send_mail
			from django.core.mail import EmailMessage
			msg = EmailMessage(subject, t.render(c), sender, recipients)
			msg.content_subtype = "html"  # Main content is now text/html
			msg.send()
		except User.DoesNotExist:
			print "Fail"
		
def openhouse():
	user = Registration.objects.all()
	for entry in user:
		entry.created_date = '2008-12-09'
		entry.save()
		
def lortest():
	lor = Recommendation.objects.filter(application=170)
	for entry in lor:
		entry.pk
			
def stats():
	app = Application.objects.all()
	app_sub = Application.objects.filter(submitted=1)
	lor = Recommendation.objects.all()
	lor_sub = Recommendation.objects.filter(recommend_date__isnull=False)
	
	for entry in lor_sub:
		print entry.recommend_date
	
	app_count = app.count()
	app_sub_count = app_sub.count()
	lor_count = lor.count()
	lor_sub_count = lor_sub.count()

	print "Total Apps: %s" % app_count
	print "Total Submitted Apps: %s" % app_sub_count 
	print "Total LOR: %s" % lor_count
	print "Total Submitted LORs: %s" % lor_sub_count
	
def names():
	lor = Recommendation.objects.all()
	for entry in lor:
		try:
			app = Application.objects.get(pk=entry.application.pk)
			entry.first_name = app.first_name
			entry.last_name = app.last_name
			entry.save()
		except Application.DoesNotExist:
				pass
		
def test():
	date = '2008-12-01'
	app = ApplicationStatus.objects.filter(submitted=1, submitted_date__gte=date)
	for entry in app:
		addy = Application.objects.get(pk=entry.application.pk)
		try:
			old_user = UserSetup.objects.get(new_pk=addy.user.pk)
			pass
		except UserSetup.DoesNotExist:
			print addy.first_name
		
		
def social():
	appstatus = ApplicationStatus.objects.all()
	for entry in appstatus:
		try:
			app = Application.objects.get(pk=entry.application.pk)
			entry.social = app.social
			entry.save()
		except Application.DoesNotExist:
			print "Fail %s" % (entry.pk)

def delete():
	appstatus = ApplicationStatus.objects.all()
	for entry in appstatus:
		if entry.pk == 47 or entry.pk == 46:
			entry.delete()
		else:
			pass

def submitted():
	appstatus = ApplicationStatus.objects.all()
	for entry in appstatus:
		try:
			app = Application.objects.get(pk=entry.application.pk)
			entry.submitted = app.submitted
			entry.submitted_date = app.submitted_date
			entry.save()
		except Application.DoesNotExist:
			print "Fail %s" % (entry.pk)
	
def password():
	olduser = UserSetup.objects.all()
	for entry in olduser:
		try:
			user = User.objects.get(pk=entry.new_pk_id)
			try:
				app = Application.objects.get(user=user.pk)
				string = ''
				for i in range(6):
					string += random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
		
				user.set_password(string)
				user.save()
				email = user.email
				app_fn = user.first_name
				app_ln = user.last_name	
				app_un = user.username
				t = loader.get_template('supapp/app_newemail.html')
				c = Context({
					'app_fn': app_fn,
					'app_ln': app_ln,
					'app_un': app_un,
					'app_pw': string,
				})
										
				subject = "UC Supplemental Application Update"
				recipients = [email]
				sender = 'sopwebmail@ucwv.edu'
				#message = 
								 
				from django.core.mail import send_mail
				from django.core.mail import EmailMessage
				msg = EmailMessage(subject, t.render(c), sender, recipients)
				msg.content_subtype = "html"  # Main content is now text/html
				msg.send()
			except Application.DoesNotExist:
				pass
		except User.DoesNotExist:
			pass
			

def test1():
	user = User.objects.filter(is_staff=True)
	for entry in user:
		if entry.pk == 1:
			string = ''
			for i in range(6):
				string += random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
	
			entry.set_password(string)
			entry.save()
			email = entry.email
			app_fn = entry.first_name
			app_ln = entry.last_name	
			app_un = entry.username
			t = loader.get_template('supapp/app_newemail.html')
			c = Context({
				'app_fn': app_fn,
				'app_ln': app_ln,
				'app_un': app_un,
				'app_pw': string,
			})
									
			subject = "UC Supplemental Application Update"
			recipients = [email]
			sender = 'sopwebmail@ucwv.edu'
			#message = 
							 
			from django.core.mail import send_mail
			from django.core.mail import EmailMessage
			msg = EmailMessage(subject, t.render(c), sender, recipients)
			msg.content_subtype = "html"  # Main content is now text/html
			msg.send()
		else:
			pass
		
def pwreset():			
	string = ''
	user = User.objects.get(pk=392)
	
	string = ''
	for i in range(6):
		string += random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

	user.set_password(string)
	user.save()
	email = user.email
	app_fn = user.first_name
	app_ln = user.last_name	
	app_un = user.username
	t = loader.get_template('supapp/app_newemail.html')
	c = Context({
		'app_fn': ap_fn,
		'app_ln': ap_ln,
		'app_un': ap_un,
		'app_pw': string,
	})
						
	subject = "UC Supplemental Application Update"
	recipients = [email]
	sender = 'sopwebmail@ucwv.edu'
	#message = 
					 
	from django.core.mail import send_mail
	send_mail(subject, t.render(c), sender, recipients)
				
def status():
	app = Application.objects.all()
	for entry in app:
		if entry.pk > 208:
			try:
				status = ApplicationStatus.objects.get(application=entry.pk)
			except ApplicationStatus.DoesNotExist:
				newstatus = ApplicationStatus()
				newstatus.application = Application.objects.get(pk=entry.pk)
				newstatus.first_name = entry.first_name
				newstatus.last_name = entry.last_name
				newstatus.initial_status = 3
				newstatus.save()
		else:
			pass		
			
def email():
	users = User.objects.all()
	for user in users:
		try:
			app = Application.objects.get(user=user.pk)
			user.first_name = app.first_name
			user.last_name = app.last_name
			user.save()
		except Application.DoesNotExist:
			pass
			
def user_setup():
	users = UserSetup.objects.all()
	for entry in users:
		try:
			user = User.objects.get(username=entry.username)
			entry.new_pk = User.objects.get(username=entry.username)
			entry.save()
		except User.DoesNotExist:
			pass

def education():
	edu = EducationSetup.objects.all()
	for entry in edu:
		try:
			user = UserSetup.objects.get(olduser=entry.olduser)
			#user1 = User.objects.get(pk=user.user)
			try:
				entry.user = User.objects.get(pk=user.new_pk_id)
				entry.save()
			except User.DoesNotExist:
				pass
		except UserSetup.DoesNotExist:
			pass
			
def education2():
	edu = EducationSetup.objects.all()
	for entry in edu:
		try:
			app = Application.objects.get(user=entry.user)
			entry.application = Application.objects.get(user=entry.user)
			entry.save()
		except Application.DoesNotExist:
			pass
			
def education3():
	edu = EducationSetup.objects.all()
	for entry in edu:
		try:
			app = Application.objects.get(pk=entry.application_id)
			new = Education()
			new.application = Application.objects.get(pk=entry.application_id)
			new.school_type = entry.school_type
			new.degree_earned = entry.degree_earned
			new.school = entry.school
			new.school_city = entry.school_city
			new.school_state = entry.school_state
			new.school_attended = entry.school_attended
			new.school_graduation = entry.school_graduation
			new.save()
		except Application.DoesNotExist:
			pass

def education4():
	edu = Education.objects.filter(application__isnull=False)
	for entry in edu:
		try:
			app = Application.objects.get(pk=entry.application.pk)
			try:
				edu_dup = Education.objects.get(application=app.pk, school=entry.school)
				print "%s: %s = %s" % (entry.application, entry.school, edu_dup.school)
			except Education.DoesNotExist:
				pass
		except Application.DoesNotExist:
			pass

def education5():
	edu = Education.objects.filter(application__isnull=False)
	for entry in edu:
		try:
			app = Application.objects.get(pk=entry.application.pk)
			try:
				edu_dup = Education.objects.filter(application=app.pk, school=entry.school)
				totals = edu_dup.count()
				x = 0
				for edu in edu_dup:
					x += 1
					if x == 1:
						pass
					else:
						edu.delete()
			except Education.DoesNotExist:
				pass
		except Application.DoesNotExist:
			pass	
									
def work():
	work = EmploymentSetup.objects.all()
	for entry in work:
		try:
			user = UserSetup.objects.get(olduser=entry.olduser)
			#user1 = User.objects.get(pk=user.user)
			try:
				entry.user = User.objects.get(pk=user.new_pk_id)
				entry.save()
			except User.DoesNotExist:
				pass
		except UserSetup.DoesNotExist:
			pass
			
def work2():
	work = EmploymentSetup.objects.all()
	for entry in work:
		try:
			app = Application.objects.get(user=entry.user)			
			dup = Employment.objects.filter(application=app.pk, employ_company=entry.employ_company)
			totals = dup.count()
			if totals > 0:
				pass
			else:
				entry.application = Application.objects.get(user=entry.user)
				entry.save()			
		except Application.DoesNotExist:
			pass
			
def work3():
	work = EmploymentSetup.objects.all()
	for entry in work:
		try:
			app = Application.objects.get(pk=entry.application_id)
			new = Employment()
			new.application = Application.objects.get(pk=entry.application_id)
			new.employ_company = entry.employ_company
			new.employ_position = entry.employ_position
			new.employ_duties = entry.employ_duties
			new.employ_dates = entry.employ_dates
			new.save()
		except Application.DoesNotExist:
			pass

def work4():
	work = Employment.objects.filter(application__isnull=False)
	for entry in work:
		try:
			app = Application.objects.get(pk=entry.application.pk)
			try:
				work_dup = Employment.objects.get(application=app.pk, employ_company=entry.employ_company)
				print "%s: %s = %s" % (entry.application, entry.employ_company, work_dup.employ_company)
			except Employment.DoesNotExist:
				pass
		except Application.DoesNotExist:
			pass
			
def work5():
	work = Employment.objects.filter(application__isnull=False)
	for entry in work:
		try:
			app = Application.objects.get(pk=entry.application.pk)
			try:
				work_dub = Employment.objects.filter(application=app.pk, employ_company=entry.employ_company)
				totals = work_dub.count()
				x = 0
				for work in work_dub:
					x += 1
					if x == 1:
						pass
					else:
						work.delete()
			except Employment.DoesNotExist:
				pass
		except Application.DoesNotExist:
			pass	
						
def edufix():
	edu = Education.objects.all()
	for entry in edu:
		try:
			app = Application.objects.get(pk=entry.application_id)
			user = User.objects.get(pk=app.user_id)
			try:
				olduser = UserSetup.objects.get(new_pk=user.pk)
				if entry.school_type == 1:
					entry.school_type = 2
					entry.save()
				else:
					entry.school_type = 1
					entry.save()
			except UserSetup.DoesNotExist:
				pass
		except Application.DoesNotExist:
				pass
				
def award():
	award = AwardsSetup.objects.all()
	for entry in award:
		try:
			user = UserSetup.objects.get(olduser=entry.olduser)
			#user1 = User.objects.get(pk=user.user)
			try:
				entry.user = User.objects.get(pk=user.new_pk_id)
				entry.save()
			except User.DoesNotExist:
				pass
		except UserSetup.DoesNotExist:
			pass
			
def award2():
	award = AwardsSetup.objects.all()
	for entry in award:
		try:
			app = Application.objects.get(user=entry.user)			
			dup = Awards.objects.filter(application=app.pk, award_title=entry.award_title)
			totals = dup.count()
			if totals > 0:
				pass
			else:
				entry.application = Application.objects.get(user=entry.user)
				entry.save()			
		except Application.DoesNotExist:
			pass
			
def award3():
	award = AwardsSetup.objects.all()
	for entry in award:
		try:
			app = Application.objects.get(pk=entry.application_id)
			new = Awards()
			new.application = Application.objects.get(pk=entry.application_id)
			new.award_title = entry.award_title
			new.award_date = entry.award_date
			new.award_basis = entry.award_basis
			new.save()
		except Application.DoesNotExist:
			pass

def award4():
	award = Awards.objects.filter(application__isnull=False)
	for entry in award:
		try:
			app = Application.objects.get(pk=entry.application.pk)
			try:
				award_dup = Awards.objects.get(application=app.pk, award_title=entry.award_title)
				print "%s: %s = %s" % (entry.application, entry.award_title, award_dup.award_title)
			except Awards.DoesNotExist:
				pass
		except Application.DoesNotExist:
			pass
			
def award5():
	award = Awards.objects.filter(application__isnull=False)
	for entry in award:
		try:
			app = Application.objects.get(pk=entry.application.pk)
			try:
				award_dub = Awards.objects.filter(application=app.pk, award_title=entry.award_title)
				totals = award_dub.count()
				x = 0
				for award in award_dub:
					x += 1
					if x == 1:
						pass
					else:
						award.delete()
			except Awards.DoesNotExist:
				pass
		except Application.DoesNotExist:
			pass	
									
def club():
	club = ClubsSetup.objects.all()
	for entry in club:
		try:
			user = UserSetup.objects.get(olduser=entry.olduser)
			#user1 = User.objects.get(pk=user.user)
			try:
				entry.user = User.objects.get(pk=user.new_pk_id)
				entry.save()
			except User.DoesNotExist:
				pass
		except UserSetup.DoesNotExist:
			pass
			
def club2():
	club = ClubsSetup.objects.all()
	x = 0
	for entry in club:
		try:
			app = Application.objects.get(user=entry.user)			
			dup = Clubs.objects.filter(application=app.pk, club_organization=entry.club_organization)
			totals = dup.count()
			if totals > 1:
				pass
			else:
				entry.application = Application.objects.get(user=entry.user)
				entry.save()			
		except Application.DoesNotExist:
			pass
			
def club3():
	club = ClubsSetup.objects.filter(application__isnull=False)
	for entry in club:
		try:
			app = Application.objects.get(pk=entry.application_id)
			new = Clubs()
			new.application = Application.objects.get(pk=entry.application_id)
			new.club_organization = entry.club_organization
			new.club_role = entry.club_role
			new.club_dates = entry.club_dates
			new.save()
		except Application.DoesNotExist:
			pass

def club4():
	club = Clubs.objects.filter(application__isnull=False)
	for entry in club:
		try:
			app = Application.objects.get(pk=entry.application.pk)
			try:
				club_dup = Clubs.objects.get(application=app.pk, club_organization=entry.club_organization)
				print "%s: %s = %s" % (entry.application, entry.club_organization, club_dup.club_organization)
			except Clubs.DoesNotExist:
				pass
		except Application.DoesNotExist:
			pass
			
def club5():
	club = Clubs.objects.filter(application__isnull=False)
	for entry in club:
		try:
			app = Application.objects.get(pk=entry.application.pk)
			try:
				club_dub = Clubs.objects.filter(application=app.pk, club_organization=entry.club_organization)
				totals = club_dub.count()
				x = 0
				for club in club_dub:
					x += 1
					if x == 1:
						pass
					else:
						club.delete()
			except Clubs.DoesNotExist:
				pass
		except Application.DoesNotExist:
			pass	
			
def vol():
	vol = VolunteerSetup.objects.all()
	for entry in vol:
		try:
			user = UserSetup.objects.get(olduser=entry.olduser)
			#user1 = User.objects.get(pk=user.user)
			try:
				entry.user = User.objects.get(pk=user.new_pk_id)
				entry.save()
			except User.DoesNotExist:
				pass
		except UserSetup.DoesNotExist:
			pass
			
def vol2():
	vol = VolunteerSetup.objects.all()
	for entry in vol:
		try:
			app = Application.objects.get(user=entry.user)			
			dup = Volunteer.objects.filter(application=app.pk, vol_organization=entry.vol_organization)
			totals = dup.count()
			if totals > 0:
				pass
			else:
				entry.application = Application.objects.get(user=entry.user)
				entry.save()			
		except Application.DoesNotExist:
			pass
			
def vol3():
	vol = VolunteerSetup.objects.filter(application__isnull=False)
	for entry in vol:
		try:
			app = Application.objects.get(pk=entry.application_id)
			new = Volunteer()
			new.application = Application.objects.get(pk=entry.application_id)
			new.vol_organization = entry.vol_organization
			new.vol_duties = entry.vol_duties
			new.vol_dates = entry.vol_dates
			new.vol_duration = entry.vol_duration
			new.save()
		except Application.DoesNotExist:
			pass
			
def vol4():
	vol = Volunteer.objects.filter(application__isnull=False)
	for entry in vol:
		try:
			app = Application.objects.get(pk=entry.application.pk)
			try:
				vol_dup = Volunteer.objects.get(application=app.pk, vol_organization=entry.vol_organization)
				print "%s: %s = %s" % (entry.application, entry.vol_organization, vol_dup.vol_organization)
			except Volunteer.DoesNotExist:
				pass
		except Application.DoesNotExist:
			pass	
					
def vol5():
	vol = Volunteer.objects.filter(application__isnull=False)
	for entry in vol:
		try:
			app = Application.objects.get(pk=entry.application.pk)
			try:
				vol_dub = Volunteer.objects.filter(application=app.pk, vol_organization=entry.vol_organization)
				totals = vol_dub.count()
				x = 0
				for club in vol_dub:
					x += 1
					if x == 1:
						pass
					else:
						club.delete()
			except Volunteer.DoesNotExist:
				pass
		except Application.DoesNotExist:
			pass