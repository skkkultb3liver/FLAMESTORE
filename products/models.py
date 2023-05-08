from django.db import models
from django.db.models import Avg
from django.urls import reverse

from categories.models import ProductCategory
from accounts.models import *


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


    def calc_avg_rating(self):
        reviews = ReviewsRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0

        if reviews['average'] is not None:
            avg = float(reviews['average'])

        return round(avg, 1)

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


class ReviewsRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=128, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.PositiveIntegerField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

    def get_created_at(self):
        return self.created_at.date().strftime('%d.%m.%Y')

    def get_updated_at(self):
        return self.updated_at.date().strftime('%d.%m.%Y')
