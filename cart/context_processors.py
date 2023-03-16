from .models import CartItem

def menu_cart_items(requests):
    cart_items = CartItem.objects.all()
    return dict(cart_items=cart_items)