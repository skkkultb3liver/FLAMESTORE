from django.contrib import admin
from django.utils.safestring import mark_safe

from products.models import *


# Register your models here.

@admin.register(ProductCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


@admin.register(AdditionalProductCategory)
class AdditionalCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "dress", "url")
    list_display_links = ("name",)

    list_filter = ("dress",)


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
    list_display = ("id", "name", "add_category", "url", "get_image")
    list_display_links = ("name",)
    list_filter = ("add_category",)
    search_fields = ("name", )

    readonly_fields = ("get_image", )

    inlines = [ProductImageInLine, ReviewInLine]

    save_on_top = True

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="60" height="auto">')

    get_image.short_description = "Image"


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

