from django.contrib import admin

from overview.models import OverView, PublicInformation, RoomType


class OverViewAdmin(admin.ModelAdmin):
    pass


class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ("type_name", "area")


class PublicInfoAdmin(admin.ModelAdmin):
    list_display = ("year", "is_published")


admin.site.register(OverView, OverViewAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(PublicInformation, PublicInfoAdmin)
