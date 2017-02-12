from django.shortcuts import render,redirect, get_object_or_404
from django.core.urlresolvers import reverse
from .forms import LoginForm, SignUpForm
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from .models import MyUser
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
import json
import base64
from django.db.models import Q

# Create your views here.
@require_POST
def handleLogin(request):
	if user.is_authenticated():
		return render(request,'account/base.html')
	f = LoginForm(request.POST)
	nexturl = request.POST.get('next')
	if f.is_valid():
		user = f.get_user()
		login(request, user)
		if not nexturl:
			return render(request,'account/base.html')
		else:
			return redirect(nexturl)
	else:
		loginform = f
		signupform = SignUpForm()
		data = {'loginform' : loginform, 'signupform':signupform, 'next':nexturl}
		return render(request,'account/base.html',data)

@require_POST
	def handleSignup(request):
	if user.is_authenticated():
		return redirect('home')

	f = SignUpForm(request.POST)
	if f.is_valid():
		user = f.save()
		user.is_active = False
		user.save()
		url = request.build_absolute_url(reverse('activate'))
		url = url + "?user=" + base64.b64encode(user.username.encode('utf-8')).decode('utf-8')
		message = "Welcome. Click <a href='%s>here </a> to activate" %url
		email = EmailMessage("Welcome", message, to=[user.email])
		email.send()
		#redirect to the post signup page..
		return render(request, 'account/base.html')
	else:
		signupform = f
		loginform = LoginForm()
		data = {'loginform': loginform, 'signupform':signupform, 'next':nexturl}
		return render(request, 'account/base.html', data)


@require_GET
def activateaccount(request):
	if request.user.is_authenticated():
		return redirect('home')
	username = base64.b64decode(request.GET.get('user').encode('utf-8')).decode('utf-8')
	user = get_object_or_404(MyUser,username=username)
	user.is_active=True
	user.save()
	return render(request,'account/base.html',{'form':LoginForm(), 'act':True})

@login_required
@require_GET
def home(request):
	return render(request,'account/base.html')

@require_GET
def logoutview(request):
	logout(request)
	return redirect('login')	