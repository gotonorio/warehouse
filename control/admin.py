from django.contrib import admin
# from control.models import AttendanceRecord
from control.models import ControlRecord


class ControlRecordAdmin(admin.ModelAdmin):
    list_display = ['tmp_user_flg', ]


admin.site.register(ControlRecord, ControlRecordAdmin)
