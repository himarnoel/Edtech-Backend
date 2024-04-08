from django.contrib import admin

# Register your models here.
from .models import CustomUser


class UserModelAdmin(admin.ModelAdmin):
  list_display = [ 'email', 'username'] 


admin.site.register(CustomUser, UserModelAdmin)