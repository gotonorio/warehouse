from django.contrib import admin
from overview.models import OverView
from overview.models import RoomType
from overview.models import Room


class OverViewAdmin(admin.ModelAdmin):
    pass


class RoomTypeAdmin(admin.ModelAdmin):
    pass


class RoomAdmin(admin.ModelAdmin):
    pass


admin.site.register(OverView, OverViewAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Room, RoomAdmin)
