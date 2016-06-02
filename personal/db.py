import models
from django.contrib.auth import authenticate, login
from django.db.models import Q

def login_view(request):
	login_email = request.POST.get('login_email')
	login_password = request.POST.get('login_password')
	print login_email
	qs = models.PersonalLogin.objects.filter(email_id=login_email,password=login_password)
	# print qs.pk
	if len(qs) == 0 :


		return "false"
	else:
		# print "sucess"
		return "true"



	

