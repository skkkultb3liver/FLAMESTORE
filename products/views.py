from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View

from cart.models import CartItem
from cart.views import _cart_id
from products.models import *
from .forms import ReviewForm
from categories.models import ProductCategory

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


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
        paginator = Paginator(products, 4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        pc = products.count()

    else:
        products = Product.objects.all().order_by('id')

        paginator = Paginator(products, 4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

        pc = products.count()

    context = {
        'products': paged_products,
        'product_count': pc,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, url=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise Exception

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
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


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']

        if keyword:
            products = Product.objects.order_by('-upload_date').filter(Q(name__icontains=keyword) | Q(category__name__icontains=keyword))
            pc = products.count()

    context = {
        'products': products,
        'product_count': pc,
    }

    return render(request, 'products/product_list.html', context)
