from django.contrib import admin
from Map.models import *


@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = ("name", "author_name")
    ordering = ("author", "name")

    def author_name(self, obj):
        return obj.author.username


@admin.register(FavouriteMap)
class FavouriteMapAdmin(admin.ModelAdmin):
    list_display = ("map_name", "user")

    def map_name(Self, obj):
        return obj.map.name
