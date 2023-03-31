from .models import CartItem, Cart
from .views import _cart_id


def counter(request):
    cart_item_counter = 0
    cart_items = None
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            cart_items = CartItem.objects.all().filter(cart=cart[:1])

            for cart_item in cart_items:
                cart_item_counter += cart_item.qty
        except Cart.DoesNotExist:
            cart_item_counter = 0

    return dict(cart_item_counter=cart_item_counter, cart_items=cart_items)

