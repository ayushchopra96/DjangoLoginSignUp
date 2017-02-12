from django.contrib import admin
from account.models import MyUser
# Register your models here.

class MyUserAdmin(admin.ModelAdmin):
	list_display = ("uid","username","email")
	class Meta:
		model = MyUser

admin.site.register(MyUser,MyUserAdmin)