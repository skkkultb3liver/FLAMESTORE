from django.db import models
from django.urls import reverse

from categories.models import ProductCategory


# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=256, unique=True)
    url = models.SlugField(max_length=128, blank=True, unique=True)
    poster = models.ImageField(upload_to='products_posters/', blank=True)
    description = models.TextField(max_length=568, blank=True)
    sizing = models.TextField(max_length=568, blank=True)
    fabric = models.TextField(max_length=568, blank=True)
    price = models.IntegerField()
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    stock = models.IntegerField(default=1)
    upload_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("product_detail", args=[self.category.slug, self.url])

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f'{self.name} | {self.category.name}'


variation_category_choice = (
    ('size', 'size'),
)


class VariationManager(models.Manager):
    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return f'{self.variation_value} for {self.product.name}'





class ProductImage(models.Model):
    image = models.ImageField(upload_to='products_images/', blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Product image'
        verbose_name_plural = 'Product images'

    def __str__(self):
        return f'IMAGE FOR {self.product.name}'


class RatingStar(models.Model):
    value = models.PositiveSmallIntegerField('Value', default=0)

    class Meta:
        verbose_name = 'Rating star'
        verbose_name_plural = 'Rating stars'
        ordering = ["-value"]

    def __str__(self):
        return f'{self.value}'


class Rating(models.Model):
    ip = models.CharField('IP adress', max_length=20)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='star')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='product')

    def __str__(self):
        return f'{self.star} - {self.product}'

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'


class Reviews(models.Model):
    text = models.TextField(max_length=5000)
    product = models.ForeignKey(Product, verbose_name='Product', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f'Review for {self.product}'

#
#
# class Customer(models.Model):
#
#     user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
#     phone = models.CharField(max_length=20, verbose_name='Phone number', null=True, blank=True)
#     address = models.CharField(max_length=255, verbose_name='Address', null=True, blank=True)
#
#     def __str__(self):
#         return f"Customer: {self.user.first_name} {self.user.last_name}"
