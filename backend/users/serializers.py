from djoser.serializers import UserSerializer

from users.models import User, UserFollow
from rest_framework import serializers


class UsersSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
        )


class UserFollowSerializer(serializers.ModelSerializer):
    follower = UserSerializer()
    followed = UserSerializer()

    class Meta:
        model = UserFollow
        fields = ('follower', 'followed')