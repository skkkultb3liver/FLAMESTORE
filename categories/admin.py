from django.contrib import admin
from .models import ProductCategory


# Register your models here.

@admin.register(ProductCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    list_display_links = ("name",)


