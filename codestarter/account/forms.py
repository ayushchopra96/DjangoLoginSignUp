from django import forms
from django.contrib.auth import authenticate
from .models import MyUser

class LoginForm(forms.Form):
	username = forms.CharField(max_length=200,null=False,blank=False,required=True)
	password = forms.CharField(widget=forms.PasswordInput)
	
	def __init__(self,*args,**kwargs):
		self.user_cache = None
		super(LoginForm,self).__init__(*args,**kwargs)

	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')

		if username and password:
			self.user_cache = authenticate(username=username, password=password)
			if self.user_cache is None:
				raise forms.ValidationError("Enter Correct Username and Password")
			elif not self.user_cache.is_active:
				raise forms.ValidationError("The account is inactive")
		return self.cleaned_data

	def get_user(self):
		return self.user_cache


class SignUpForm(forms.ModelForm):
	password1 = forms.CharField(label = "Password", widget=forms.PasswordInput)
	password2 = forms.CharField(label = "Confirm Password", widget = forms.PasswordInput)
	
	def __init__(self,*args,**kwargs):
		super(SignUpForm,self).__init__(*args,**kwargs)
		self.fields['email'].required=True
		self.fields['phone'].required=True

	def clean_password(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if password1 and password2 and password1!=password2:
			raise forms.ValidationError("Passwords dont match")
		return password2

	def clean_email(self):
		email_data = self.cleaned_data.get('email')
		if email_data and len(MyUser.objects.filter(email=email_data)) > 0:
			raise forms.ValidationError("User with email already exists")
		return email_data

	def save(self, commit=True):
		user = super(SignUpForm,self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user

	class Meta:
		model = MyUser
		fields = ['username','email','phone','github']