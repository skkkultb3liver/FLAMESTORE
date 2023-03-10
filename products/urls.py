from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_view, name='store'),
    path("<slug:category_slug>/", views.product_view, name='products_by_category'),
    path("<slug:category_slug>/<slug:product_slug>/", views.product_detail, name='product_detail'),
    # path("", views.ProductsView.as_view(), name='catalog'),
    # path("filter/", views.FilterProductsView.as_view(), name="filter"),
    # path("<slug:slug>/", views.ProductsDetails.as_view(), name="product"),
    # path("review/<int:pk>/", views.AddReview.as_view(), name="add_review")
]