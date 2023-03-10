from django.db import models
from django.urls import reverse
# Create your models here.



class ProductCategory(models.Model):
    name = models.CharField("Genre category", max_length=64, unique=True)
    slug = models.SlugField(max_length=128, blank=True, unique=True)
    key = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = 'Product category'
        verbose_name_plural = 'Product categories'
        ordering = ['key']

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.name


