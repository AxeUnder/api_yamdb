from django.urls import path
from api.views import sign_up, TokenApiView


urlpatterns = [
    path('signup/', sign_up, name='signup'),
    path('token/', TokenApiView.as_view(), name='token_access'),
]
