from django.contrib import admin

# Register your models here.
from .models import CustomUser


class UserModelAdmin(admin.ModelAdmin):
  list_display = [ 'email', 'username','fullName','email_verified',] 


admin.site.register(CustomUser, UserModelAdmin)