from django.contrib import admin
from django.utils.safestring import mark_safe

from products.models import *
from categories.models import ProductCategory


# Register your models here.

class ReviewInLine(admin.StackedInline):
    model = Reviews
    extra = 1


class ProductImageInLine(admin.TabularInline):
    model = ProductImage
    extra = 1

    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="auto" height="100">')

    get_image.short_description = "Image"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "stock", "price", 'category', "modified_date", "url", "get_image")
    prepopulated_fields = {"url": ("name",)}
    list_display_links = ("name",)
    list_filter = ("category", )
    search_fields = ("name", )

    readonly_fields = ("get_image", )

    inlines = [ProductImageInLine, ReviewInLine]

    save_on_top = True

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="60" height="auto">')

    get_image.short_description = "Image"


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "variation_value", "is_active")
    list_display_links = ("id", "product")
    list_editable = ("is_active", )
    list_filter = ("product", "is_active",)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "get_image")
    list_display_links = ("id", "product")
    readonly_fields = ("get_image", )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="45" height="auto">')

    get_image.short_description = "Image"


@admin.register(Reviews)
class Reviewadmin(admin.ModelAdmin):
    list_display = ("id", "product")
    list_display_links = ("id",)


admin.site.register(Rating)
admin.site.register(RatingStar)

