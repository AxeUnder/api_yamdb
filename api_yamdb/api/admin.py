from django.conf import settings as s
from django.contrib import admin

from reviews.models import Category, Genre, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category', 'genre')
    list_editable = ('text',)
    search_fields = ('text',)


class CategoryAdmin(admin.ModelAdmin):
    pass


class GenreAdmin(admin.ModelAdmin):
    pass


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryeAdmin)
admin.site.register(Genre, GenreAdmin)
