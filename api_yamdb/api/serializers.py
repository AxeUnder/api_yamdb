from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

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


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=False)
    genre = GenreSerializer(read_only=True, many=True)

    # продолжение следует ..

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    pass


class CommentSerializer(serializers.ModelSerializer):
    """Serializer модели Comment."""
    review = serializers.SlugRelatedField(
        slug_field='review_id',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('pub_date',)


class UserSignUpSerializer(serializers.Serializer):
    username = serializers.RegexField(max_length=150,
                                      regex=r'^[\w.@+-]+\Z',
                                      required=True)
    email = serializers.EmailField(max_length=150,
                                   required=True)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Username "me" запрещён к использованию'
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(max_length=150,
                                      regex=r'^[\w.@+-]+\Z', required=True)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(max_length=150,
                                      regex=r'^[\w.@+-]+\Z',
                                      required=True)
    email = serializers.EmailField(max_length=150,
                                   required=True)

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')
        validators = [UniqueTogetherValidator(
            queryset=User.objects.all(),
            fields=('username', 'email')
        )]


class UserEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')
        read_only_fields = ('role',)