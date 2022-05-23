from django.contrib import admin
from control.models import AttendanceRecord
from control.models import ControlRecord


class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'login_time', 'logout_time']
    ordering = ('login_time', )


class ControlRecordAdmin(admin.ModelAdmin):
    list_display = ['tmp_user_flg', ]


admin.site.register(AttendanceRecord, AttendanceRecordAdmin)
admin.site.register(ControlRecord, ControlRecordAdmin)
