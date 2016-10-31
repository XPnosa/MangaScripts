from django.contrib import admin

# Register your models here.

from .models import Manga, Volume, Chapter, App_User
from .models import Manga_fav, Volume_fav, Chapter_fav, Chapter_read

# Principales
admin.site.register(Manga)
admin.site.register(Volume)
admin.site.register(Chapter)
admin.site.register(App_User)
# Secundarias
admin.site.register(Manga_fav)
admin.site.register(Volume_fav)
admin.site.register(Chapter_fav)
admin.site.register(Chapter_read)
