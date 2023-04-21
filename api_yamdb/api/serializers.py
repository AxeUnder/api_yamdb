from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import User

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )


class TitleSerializerRead(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializerWrite(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        read_only=False,
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        read_only=False,
        queryset=Genre.objects.all(),
        many=True,
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer модели Review."""

    title = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Title.objects.all(),
        required=False
    )
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data

        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if Review.objects.filter(
                author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв к этому произведению.'
            )
        return data

    def validate_score(self, value):
        if 1 > value > 10:
            raise serializers.ValidationError(
                'Дайте оценку в диапазоне от 1 до 10.'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Serializer модели Comment."""

    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        exclude = ('review',)


class UserSignUpSerializer(serializers.Serializer):
    username = serializers.RegexField(
        max_length=150, regex=r'^[\w.@+-]+\Z', required=True
    )
    email = serializers.EmailField(max_length=150, required=True)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Username "me" запрещён к использованию'
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        max_length=150, regex=r'^[\w.@+-]+\Z', required=True
    )


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        max_length=150, regex=r'^[\w.@+-]+\Z', required=True
    )
    email = serializers.EmailField(
        max_length=150,
        required=True,
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Username "me" запрещён к использованию'
            )
        return value

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(), fields=('username', 'email')
            )
        ]


class UserEditSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        max_length=150, regex=r'^[\w.@+-]+\Z', required=True
    )
    email = serializers.EmailField(max_length=150, required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = ('role',)
