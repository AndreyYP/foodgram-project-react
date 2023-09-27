from http import HTTPStatus

from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet

from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, UserFollow
from .serializers import UsersSerializer, UserFollowSerializer


class UsersViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    http_method_names = ['get', 'post', 'delete', 'head']
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['POST', 'DELETE'])
    def subscribe(self, request, pk=None):
        if request.method == 'POST':
            followed_user = self.get_object()
            if UserFollow.objects.filter(user=request.user, author=followed_user).exists():
                return Response({'detail': 'Уже подписаны'}, status=status.HTTP_400_BAD_REQUEST)
            UserFollow.objects.create(user=request.user, author=followed_user)
            return Response({'status': 'subscribed'}, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            followed_user = self.get_object()
            try:
                subscription = UserFollow.objects.get(user=request.user, author=followed_user)
            except UserFollow.DoesNotExist:
                return Response({'detail': 'Вы не подписаны на этого пользователя'}, status=status.HTTP_400_BAD_REQUEST)
            subscription.delete()
            return Response({'status': 'unsubscribed'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'])
    def subscriptions(self, request):
        user_following = UserFollow.objects.filter(user=request.user)
        followed_users = [follow.author for follow in user_following]
        serializer = UsersSerializer(followed_users, many=True, context={'request': request})
        return Response(serializer.data)
