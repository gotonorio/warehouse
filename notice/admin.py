
from django.contrib import admin

from .models import News


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'comment', 'display_news', 'created_at')


admin.site.register(News, NewsAdmin)
