from django.db import models

from products.models import Product, Variation


# Create your models here.


class Cart(models.Model):
    cart_id = models.CharField(max_length=128, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variation, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.qty

    def __str__(self):
        return f'Cart product: {self.product}'