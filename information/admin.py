from django.contrib import admin

from information.models import Information, InformationType


class InformationAdmin(admin.ModelAdmin):
    list_display = ("title", "display_info", "members_only", "type_name", "sequense")


class InformationTypeAdmin(admin.ModelAdmin):
    list_display = ("type_name", "is_alive")


# Register your models here.
admin.site.register(InformationType, InformationTypeAdmin)
admin.site.register(Information, InformationAdmin)
