from django.contrib import admin


# Register your models here.
from .models import Enrollment, Transaction




admin.site.register(Enrollment)
admin.site.register(Transaction)