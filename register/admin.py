from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# from register.models import ControlRecord


# class ControlRecordAdmin(admin.ModelAdmin):
#     list_display = ['name', 'tmp_user_flg', ]


admin.site.register(User, UserAdmin)
# admin.site.register(ControlRecord, ControlRecordAdmin)
