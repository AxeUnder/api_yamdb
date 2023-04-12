from django.urls import include, path
from rest_framework import routers

# этот и другие комментарии перед отправкой на ревью я удалю
# цифра 1 для "routers1" введена по замечанию ревьюера к предыд. спринту
# т.к. у нас может быть несколько версий
router1 = routers.DefaultRouter()
router1.register('titles', TitleViewSet, basename='titles')
router1.register('categories', CategoryViewSet, basename='categories')
router1.register('genres', GenreViewSet, basename='genres')


urlpatterns = [
    path('v1/', include(router_1.urls)),
]
