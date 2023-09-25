from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from users import views
from users.views import UserViewSet

router = DefaultRouter()

router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/<int:pk>/subscribe/', views.UsersViewSet.as_view({'post': 'subscribe'}), name='subscribe_to_user'),
    re_path('auth/', include('djoser.urls.authtoken')),
]
