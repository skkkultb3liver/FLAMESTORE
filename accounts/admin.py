from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


# Register your models here.
@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'joined_date', 'is_active')
    readonly_fields = ('last_login', 'joined_date')
    ordering = ('-joined_date', )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()



