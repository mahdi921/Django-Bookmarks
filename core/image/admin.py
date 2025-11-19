from django.contrib import admin
from image.models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'image', 'created', 'updated']
    list_filter = ['created']
