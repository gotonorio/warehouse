from django.contrib import admin

from information.models import Information, InformationType

# Register your models here.
admin.site.register(InformationType)
admin.site.register(Information)
