from .models import ProductCategory


def menu_links(requests):
    links = ProductCategory.objects.all()
    return dict(links=links)
