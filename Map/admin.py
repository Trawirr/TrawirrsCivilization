from django.contrib import admin
from Map.models import *


@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = ("name", "author_name")
    ordering = ("author", "name")

    def author_name(self, obj):
        return obj.author.username
