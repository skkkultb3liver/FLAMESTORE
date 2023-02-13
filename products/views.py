from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import ListView, DetailView

from products.models import *
from .forms import ReviewForm


# Create your views here.

class GenreDress:

    def get_genres(self):
        return ProductCategory.objects.all()

    def get_clothing(self):
        return AdditionalProductCategory.objects.all()


class ProductsView(GenreDress, ListView):

    model = Product
    queryset = Product.objects.all()
    # template_name = "products/product_list.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context["g_categories"] = ProductCategory.objects.all()
    #     context["a_categories"] = AdditionalProductCategory.objects.all()
    #
    #     return context



class ProductsDetails(DetailView):

    model = Product
    slug_field = "url"


class Mainscreen(View):

    def get(self, request):
        title = "FLAMESTORE"

        return render(request, "mainscreen.html", {"title": title})


class AddReview(View):

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        product = Product.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.product = product
            form.save()
        return redirect(product.get_absolute_url())


class FilterProductsView(GenreDress, ListView):

    def get_queryset(self):
        queryset = Product.objects.filter(
            Q(category__in=self.request.GET.getlist("category")) |
            Q(add_category__in=self.request.GET.getlist("add_category")))
        return queryset

