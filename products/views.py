
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View

from products.models import *
from .forms import ReviewForm
from categories.models import ProductCategory


def mainscreen(request):
    title = 'FLAMESTORE'
    context = {
        'title': title
    }
    return render(request, 'mainscreen.html', context)


def product_view(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(ProductCategory, slug=category_slug)
        products = Product.objects.filter(category=categories)
        pc = products.count()

    else:
        products = Product.objects.all()
        pc = products.count()

    context = {
        'products': products,
        'product_count': pc,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, url=product_slug)
    except Exception as e:
        raise Exception

    context = {
        'single_product': single_product,
    }

    return render(request, 'products/product_detail.html', context)


class AddReview(View):

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        product = Product.objects.get(id=pk)

        if form.is_valid():
            form = form.save(commit=False)
            form.product = product
            form.save()

        return redirect(product.get_absolute_url())


