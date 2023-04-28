from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product, Variation
from .models import *
from django.contrib import messages


# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)

    #authenticated///////////////////////////////////////////////////////////////////////////////////////////////////
    if current_user.is_authenticated:

        product_variation_list = []

        if request.method == 'POST':
            size = request.POST['size']
            try:
                variation = Variation.objects.get(product=product, variation_value__iexact=size)
                product_variation_list.append(variation)
            except:
                pass

        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            ex_vars_list = []
            id_item_list = []

            for item in cart_item:
                ex_variation = item.variation.all()
                ex_vars_list.append(list(ex_variation))
                id_item_list.append(item.id)

            if product_variation_list in ex_vars_list:
                index = ex_vars_list.index(product_variation_list)
                item_id = id_item_list[index]
                item = CartItem.objects.get(product=product, id=item_id)

                if item.qty < product.stock:
                    item.qty += 1
                else:
                    messages.error(request, "You are over the limit")
                item.save()

            else:
                item = CartItem.objects.create(product=product, qty=1, user=current_user)

                if len(product_variation_list) > 0:
                    item.variation.clear()
                    item.variation.add(*product_variation_list)

                item.save()

        else:
            cart_item = CartItem.objects.create(product=product, qty=1, user=current_user)

            if len(product_variation_list) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation_list)

            cart_item.save()

        return redirect('cart')

    # not authenticated////////////////////////////////////////////////////////////////////////////////////////////
    else:

        product_variation_list = []

        if request.method == 'POST':
            size = request.POST['size']
            try:
                variation = Variation.objects.get(product=product, variation_value__iexact=size)
                product_variation_list.append(variation)
            except:
                pass

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))

        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))

        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            ex_vars_list = []
            id_item_list = []

            for item in cart_item:
                ex_variation = item.variation.all()
                ex_vars_list.append(list(ex_variation))
                id_item_list.append(item.id)

            print(ex_vars_list)

            if product_variation_list in ex_vars_list:
                index = ex_vars_list.index(product_variation_list)
                item_id = id_item_list[index]
                item = CartItem.objects.get(product=product, id=item_id)

                if item.qty < product.stock:
                    item.qty += 1
                else:
                    messages.error(request, "You are over the limit")
                item.save()

            else:
                item = CartItem.objects.create(product=product, qty=1, cart=cart)

                if len(product_variation_list) > 0:
                    item.variation.clear()
                    item.variation.add(*product_variation_list)

                item.save()

        else:
            cart_item = CartItem.objects.create(product=product, qty=1, cart=cart)

            if len(product_variation_list) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation_list)

            cart_item.save()

        return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):

    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

    cart_item.delete()
    return redirect('cart')


def remove_cart(request, product_id, cart_item_id):

    product = get_object_or_404(Product, id=product_id)

    try:

        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

        if cart_item.qty > 1:
            cart_item.qty -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass

    return redirect('cart')


def cart(request, total=0, qty=0, cart_items=None):
    try:
        grand_total = 0
        tax = 0

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.qty
            qty += cart_item.qty

        tax = int((2 * total) // 100)
        grand_total = tax + total

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'qty': qty,
        'cart_items': cart_items,
        'grand_total': grand_total,
        'tax': tax,
    }
    return render(request, 'products/cart.html', context)


@login_required(login_url='login')
def checkout(request, total=0, qty=0, cart_items=None):
    try:
        grand_total = 0
        tax = 0

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.qty
            qty += cart_item.qty
        tax = (2 * total) / 100
        grand_total = tax + total

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'qty': qty,
        'cart_items': cart_items,
        'grand_total': grand_total,
        'tax': tax,
    }

    return render(request, 'products/checkout.html', context)
