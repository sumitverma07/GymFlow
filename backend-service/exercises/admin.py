from django.contrib import admin

from .models import Exercise

# Register your models here.


class ExersiceAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


admin.site.register(Exercise, ExersiceAdmin)
