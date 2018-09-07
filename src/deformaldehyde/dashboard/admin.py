from django.contrib import admin

from .models import Category, Links, AreaTag, Tag, SiteSettings


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = ('create_time', 'update_time')
    list_display = ('id', 'name', 'sequence', 'slug')
    list_editable = ['sequence']


@admin.register(Links)
class LinksAdmin(admin.ModelAdmin):
    exclude = ('slug', 'create_time', 'update_time')
    list_display = ('name', 'url')


@admin.register(AreaTag)
class AreaTagAdmin(admin.ModelAdmin):
    exclude = ('create_time', 'update_time')
    list_display = ('id', 'name', 'slug')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    exclude = ('create_time', 'update_time')
    list_display = ('id', 'name', 'slug')


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    pass

