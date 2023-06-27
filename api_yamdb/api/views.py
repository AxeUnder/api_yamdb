from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User

from api.permissions import (
    AdminOrModerOrUserOrReadOnly,
    AdminOrReadOnly,
    IsAdmin,
    IsAuthorOrReadOnlyPermission,
)
from api.mixins import CreateListViewSet
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializerRead,
    TitleSerializerWrite,
    TokenSerializer,
    UserEditSerializer,
    UserSerializer,
    UserSignUpSerializer,
)
from reviews.filters import TitleFilter
from reviews.models import Category, Genre, Review, Title


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet модели Title."""

    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleSerializerRead
        return TitleSerializerWrite


class CategoryViewSet(CreateListViewSet):
    """ViewSet модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListViewSet):
    """ViewSet модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet модели Review."""

    serializer_class = ReviewSerializer
    permission_classes = (
        AdminOrReadOnly,
        AdminOrModerOrUserOrReadOnly,
    )
    pagination_class = LimitOffsetPagination

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
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, id=self.kwargs.get('review_id')),
        )


@api_view(['POST'])
def sign_up(request):
    serializer = UserSignUpSerializer(data=request.data)
    email = request.data.get('email')
    serializer.is_valid(raise_exception=True)
    try:
        user, created = User.objects.get_or_create(**serializer.validated_data)
    except IntegrityError:
        return Response(
            'Попробуй другой email или username',
            status=status.HTTP_400_BAD_REQUEST,
        )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Token Token Token',
        confirmation_code,
        'Yamdb',
        [email],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


class TokenApiView(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.initial_data.get('username')
            user = get_object_or_404(User, username=username)
            confirmation_code = serializer.initial_data.get(
                'confirmation_code'
            )
            if not default_token_generator.check_token(
                user, confirmation_code
            ):
                return Response(
                    'Неправильный код', status=status.HTTP_400_BAD_REQUEST
                )
            token = RefreshToken.for_user(user)
            return Response(
                {'token': str(token.access_token)},
                status=status.HTTP_201_CREATED,
            )
        return Response('Error', status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        user = get_object_or_404(User, username=self.request.user)
        serializer = UserEditSerializer(user)
        if request.method == 'PATCH':
            serializer = UserEditSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            User.objects.get_or_create(**serializer.validated_data)
            return Response(
                serializer.validated_data, status=status.HTTP_201_CREATED
            )
        except IntegrityError:
            return Response(
                'Попробуй другой email или username',
                status=status.HTTP_400_BAD_REQUEST,
            )
