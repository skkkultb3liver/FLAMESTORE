from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View

from cart.models import CartItem
from cart.views import _cart_id
from orders.models import OrderProduct
from products.models import *
from categories.models import ProductCategory
from .forms import *
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator



def mainscreen(request):
    title = 'FLAMESTORE'

    products = Product.objects.order_by('-upload_date')
    context = {
        'title': title,
        'u_products': products,
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

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    reviews = ReviewsRating.objects.filter(product_id=single_product.id, status=True)




    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'order_product': orderproduct,
        'reviews': reviews,
    }

    return render(request, 'products/product_detail.html', context)





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


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        try:
            product = Product.objects.get(id=product_id)
            reviews = ReviewsRating.objects.get(user__id=request.user.id, product=product)

            form = ReviewForm(request.POST, instance=reviews)
            form.save()

            messages.success(request, "Your review has been updated")

            return redirect(url)

        except ReviewsRating.DoesNotExist:
            form = ReviewForm(request.POST)

            if form.is_valid():

                review = ReviewsRating()
                review.subject = form.cleaned_data['subject']
                review.review = form.cleaned_data['review']
                review.rating = form.cleaned_data['rating']
                review.ip = request.META.get('REMOTE_ADDR')
                review.product_id = product_id
                review.user_id = request.user.id

                review.save()

                messages.success(request, "Thank you! Your review has been submited.")

                return redirect(url)


