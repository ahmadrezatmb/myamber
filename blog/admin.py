from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import fields
from .models import post , comment , amberuser, resetpassword
# Register your models here.
class postadmin(admin.ModelAdmin):
    list_display = ('title','author' , 'date' , 'hascomment')
class resetpasswordadmin(admin.ModelAdmin):
    list_display = ('username' ,)

admin.site.register(resetpassword)
admin.site.register(amberuser)
admin.site.register(post ,postadmin)
admin.site.register(comment)