from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

# Register your models here.

admin.site.register(Payment)


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 1

    list_display = ("payment", "product", "qty", "product_price", "ordered", "get_image")


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.product.poster.url} width="60" height="auto">')

    get_image.short_description = "Image"

    list_display = ("payment", "product", "qty", "product_price", "ordered", "get_image")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "get_fullname", "email", "status", "ip_ordered", "created_at", "updated_at")
    list_display_links = ("order_number",)
    readonly_fields = ("get_fullname", "email",)

    inlines = [OrderProductInline]