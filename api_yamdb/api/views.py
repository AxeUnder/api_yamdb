from rest_framework import filters, viewsets, pagination
from rest_framework.generics import get_object_or_404

from reviews.models import Title, Category, Genre, Review


# пока создал пустые шаблоны вьюсетов
class TitleViewSet(viewsets.ModelViewSet):
    pass


class CategoryViewSet(viewsets.ModelViewSet):
    pass


class GenreViewSet(viewsets.ModelViewSet):
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet модели Review."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, id=self.kwargs.get('title_id'))
        )
