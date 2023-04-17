from django.contrib import admin

from .models import Category, Genre, Review, Title


class ReviewAdmin(admin.ModelAdmin):
    """Админ-модель отзывов."""

    list_display = (
        'pk',
        'title',
        'text',
        'author',
        'score',
        'pub_date',
    )
    list_fields = ('title', 'text', 'author')
    list_editable = ('score',)
    list_filter = ('pub_date',)


class TitleAdmin(admin.ModelAdmin):
    """Админ-модель произведений."""

    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category',
    )
    list_editable = ('description',)
    search_fields = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    """Админ-модель категорий."""

    list_display = (
        'pk',
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('slug',)
    prepopulated_fields = {'slug': ('name',)}


class GenreAdmin(admin.ModelAdmin):
    """Админ-модель жанров."""

    list_display = (
        'pk',
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('slug',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
