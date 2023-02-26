from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
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
    queryset = Product.objects.all().order_by('id')
    paginate_by = 1

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context["g_categories"] = ProductCategory.objects.all()
    #     context["a_categories"] = AdditionalProductCategory.objects.all()
    #
    #     return context


class ProductsDetails(DetailView):
    model = Product
    slug_field = "url"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["star_form"] = RatingForm()
    #     return context


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
    paginate_by = 1

    def get_queryset(self):
        queryset = Product.objects.filter(
            Q(category__in=self.request.GET.getlist("category")) &
            Q(add_category__in=self.request.GET.getlist("add_category"))
        ).distinct()

        return queryset


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["genre"] = ''.join(f'genre={x}&' for x in self.request.GET.getlist("category"))
        context["dress"] = ''.join(f'dress={x}&' for x in self.request.GET.getlist("dress"))

        return context


# class AddStarRating(View):
#
#     def get_client_ip(self, request):
#         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#         if x_forwarded_for:
#             ip = x_forwarded_for.split(',')[0]
#         else:
#             ip = request.META.get('REMOTE_ADDR')
#         return ip
#
#     def post(self, request):
#         form = RatingForm(request.POST)
#         if form.is_valid():
#             Rating.objects.update_or_create(
#                 ip=self.get_client_ip(request),
#                 product_id=int(request.POST.get("product")),
#                 defaults={'star_id': int(request.POST.get("star"))}
#             )
#             return HttpResponse(status=201)
#         else:
#             return HttpResponse(status=400)
