from django.urls import path, include
from djoser.views import TokenCreateView, TokenDestroyView

urlpatterns = [
    # path('auth/', include('djoser.urls')),
    # path('auth/token/', TokenCreateView.as_view(), name='token-create'),
    # path('auth/token/destroy/', TokenDestroyView.as_view(), name='token-destroy'),
]
# TODO