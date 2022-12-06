from django.contrib import admin
from .models import Title, Genres, Categories, CustomUser, Review, Comment


class TitlesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category_id')
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'role',
        'email',
        'first_name',
        'last_name',
        'bio'
    )
    search_fields = ('username',)
    list_per_page = 10
    list_filter = (
        'username',
        'role',
        'email',
        'bio'
    )
    fieldsets = (
        (None, {
            'fields': (
                'username',
                'role',
                'email',
                'first_name',
                'last_name',
                'bio'
            )
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Title, TitlesAdmin)
admin.site.register(Genres)
admin.site.register(Categories)
admin.site.register(Review)
admin.site.register(Comment)
