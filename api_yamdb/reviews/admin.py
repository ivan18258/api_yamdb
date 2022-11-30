from django.contrib import admin
from .models import Titles, Genres, Categories


class TitlesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category')
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


admin.site.register(Titles, TitlesAdmin)
admin.site.register(Genres)
admin.site.register(Categories)

