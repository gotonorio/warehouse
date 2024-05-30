from django.contrib import admin

from overview.models import OverView, RoomType


class OverViewAdmin(admin.ModelAdmin):
    pass


class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ("type_name", "area")


class RoomAdmin(admin.ModelAdmin):
    list_display = ("room_no", "owner", "tenant")


admin.site.register(OverView, OverViewAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
