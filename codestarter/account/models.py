from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class MyUser(AbstractUser):
	GENDER_CHOICES = (('M','Male'),('F','Female'))
	init_github = "www.github.com/"
	uid = models.IntegerField(default=0)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
	username = models.CharField(max_length=30,null=False,blank=False,unique=True)
	email = models.EmailField(null=False,blank=False)
	phone = PhoneNumberField(unique=True, null=True, blank=True, help_text=('Only Indian'))
	github = models.CharField(max_length=30,null=True)

	def __unicode__(self):
		return "@" + self.github