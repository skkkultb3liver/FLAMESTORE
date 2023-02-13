from django.urls import path
from . import views

urlpatterns = [
    path("filter/", views.FilterProductsView.as_view(), name="filter"),
    path("", views.ProductsView.as_view(), name="catalog"),
    path("<slug:slug>/", views.ProductsDetails.as_view(), name="product"),
    path("review/<int:pk>", views.AddReview.as_view(), name="add_review")
]