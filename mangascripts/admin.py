from django.contrib import admin

# Register your models here.

from .models import Manga, Volume, Chapter

admin.site.register(Manga)
admin.site.register(Volume)
admin.site.register(Chapter)
