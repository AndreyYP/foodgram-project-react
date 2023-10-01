from djoser.views import UserViewSet

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from users.models import User, UserFollow
from users.serializers import UsersSerializer, SubscriptionSerializer
from rest_framework.response import Response


class UsersViewSet(UserViewSet):
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    http_method_names = ['get', 'post', 'delete', 'head']

    def get_queryset(self):
        return User.objects.order_by('username')

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        serializer = UsersSerializer(user, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['POST', 'DELETE'])
    def subscribe(self, request, id):
        if request.method == 'POST':
            followed_user = self.get_object()
            if UserFollow.objects.filter(user=request.user, author=followed_user).exists():
                return Response({'detail': 'Уже подписаны'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = SubscriptionSerializer(followed_user, context={'request': request})
            UserFollow.objects.create(user=request.user, author=followed_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            followed_user = self.get_object()
            try:
                subscription = UserFollow.objects.get(user=request.user, author=followed_user)
            except UserFollow.DoesNotExist:
                return Response({'detail': 'Вы не подписаны на этого пользователя'}, status=status.HTTP_400_BAD_REQUEST)
            subscription.delete()
            return Response({'status': 'unsubscribed'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        follows = User.objects.filter(followed__user=user)
        paginator = PageNumberPagination()
        paginator.page_size = 6
        paginated_follows = paginator.paginate_queryset(follows, request)
        serializer = SubscriptionSerializer(paginated_follows, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)
