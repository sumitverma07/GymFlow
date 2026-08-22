from django.contrib import admin

from .models import ExerciseImage


# Register your models here.
class ExersiceImagesAdmin(admin.ModelAdmin):
    list_display = ["id", "image_url"]


admin.site.register(ExerciseImage, ExersiceImagesAdmin)
