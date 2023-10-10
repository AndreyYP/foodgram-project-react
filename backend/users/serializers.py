from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers

from users.models import User, UserFollow


class UsersSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserFollow.objects.filter(
                user=request.user, author=obj).exists()
        return False

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request:
            return UserFollow.objects.filter(
                user=request.user, author=obj).exists()
        return False

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_recipes(self, obj):
        from recipes.serializers import FavoriteSerializer

        request = self.context.get('request')
        context = {'request': request}
        queryset = obj.recipes.all()
        return FavoriteSerializer(queryset, context=context, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class RegistrationSerializer(UserCreateSerializer, SubscriptionSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'password')
