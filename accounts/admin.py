from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import *


# Register your models here.
@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'joined_date', 'is_active')
    readonly_fields = ('last_login', 'joined_date')
    ordering = ('-joined_date',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    def avatar(self, obj):
        return mark_safe(f'<img src="{obj.profile_picture.url}" width="30px" style="border-radius: 50%"')

    avatar.short_desciption = 'Profile picture'
    list_display = ('avatar', 'user', 'country', 'city')
    list_display_links = ('user',)


