from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from recipes.views import RecipeViewSet, TagViewSet, IngredientViewSet
from users import views
from users.views import UsersViewSet

router = DefaultRouter()

router.register(r'users', UsersViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'tags', TagViewSet)
router.register(r'ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/subscriptions/', UsersViewSet.as_view({'get': 'subscriptions'}), name='subscriptions'),
    path('users/<int:pk>/subscribe/', views.UsersViewSet.as_view({'post': 'subscribe', 'delete': 'unsubscribe'}), name='subscribe_unsubscribe'),

    re_path('auth/', include('djoser.urls.authtoken')),
]
