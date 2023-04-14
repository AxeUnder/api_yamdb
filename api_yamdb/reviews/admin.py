from django.contrib import admin
from .models import Review, Title, Category, Genre


class ReviewAdmin(admin.ModelAdmin):
    """Админ-модель отзывов."""
    list_display = (
        'pk',
        'title',
        'text'
        'author',
        'score',
        'pub-date'
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
    pass


class GenreAdmin(admin.ModelAdmin):
    """Админ-модель жанров."""
    pass


admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
