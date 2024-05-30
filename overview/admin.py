from django.contrib import admin

from overview.models import OverView, RoomType


class OverViewAdmin(admin.ModelAdmin):
    pass


class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ("type_name", "area")


admin.site.register(OverView, OverViewAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
