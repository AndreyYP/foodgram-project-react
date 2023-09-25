from djoser.views import UserViewSet

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, UserFollow
from .serializers import UsersSerializer


class UsersViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    http_method_names = ['get', 'post', 'delete', 'head']
    lookup_field = 'pk'

    @action(detail=True, methods=['POST'])
    def subscribe(self, request, pk=None):
        followed_user = self.get_object()

        if UserFollow.objects.filter(user=request.user, author=followed_user).exists():
            return Response({'detail': 'You are already following this user.'}, status=status.HTTP_400_BAD_REQUEST)

        UserFollow.objects.create(user=request.user, author=followed_user)

        return Response({'status': 'subscribed'}, status=status.HTTP_201_CREATED)
