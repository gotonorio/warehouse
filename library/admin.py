from django.contrib import admin
from library.models import BigCategory, Category, File


class BigCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'created_at')


admin.site.register(BigCategory, BigCategoryAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'created_at')


admin.site.register(Category, CategoryAdmin)


class FileAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'order', 'created_at')


admin.site.register(File, FileAdmin)
