from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product", "qty", "is_active")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "cart_id", "date_added")
    list_display_links = ("cart_id", )


