from django.urls import include, path
from rest_framework import routers

from .views import TitleViewSet, CategoryViewSet, GenreViewSet, ReviewViewSet, CommentViewSet

# этот и другие комментарии перед отправкой на ревью я удалю
# цифра 1 для "routers1" введена по замечанию ревьюера к предыд. спринту
# т.к. у нас может быть несколько версий
router_v1 = routers.DefaultRouter()
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/', ReviewViewSet, basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/', CommentViewSet, basename='comments')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
