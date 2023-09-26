from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, UserFollow
from django.contrib.admin import register


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role')
    list_filter = ('username', 'email')


#@register(UserFollow)
#class CustomFollowAdmin(UserAdmin):
#    list_display = ('user', 'author')
