from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    # path('auth/token/', TokenCreateView.as_view(), name='token-create'),
    # path('auth/token/destroy/', TokenDestroyView.as_view(), name='token-destroy'),
]
