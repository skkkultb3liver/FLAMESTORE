from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_view, name='store'),
    path("category/<slug:category_slug>/", views.product_view, name='products_by_category'),
    path("category/<slug:category_slug>/<slug:product_slug>/", views.product_detail, name='product_detail'),
    path("search/", views.search, name='search'),
]