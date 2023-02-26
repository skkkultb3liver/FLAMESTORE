from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProductsView.as_view(), name="catalog"),
    path("filter/", views.FilterProductsView.as_view(), name="filter"),
    path("<slug:slug>/", views.ProductsDetails.as_view(), name="product"),
    path("review/<int:pk>", views.AddReview.as_view(), name="add_review")
]