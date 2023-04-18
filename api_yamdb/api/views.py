from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, pagination, viewsets
from rest_framework.generics import get_object_or_404

from api.mixins import CreateListViewSet
from api.permissions import AdminOrReadOnly
from api.serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer, ReviewSerializer,
    TitleSerializer,
)
from reviews.models import Category, Comment, Genre, Review, Title


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)


class CategoryViewSet(CreateListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)


class GenreViewSet(CreateListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet модели Review."""

    serializer_class = ReviewSerializer
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, id=self.kwargs.get('title_id')),
        )


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet модели Comment."""
    serializer_class = CommentSerializer
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Title, id=self.kwargs.get('review_id')),
        )
