from django.utils.safestring import mark_safe
from django import template
register = template.Library()


@register.simple_tag
def star_rating(rating):
    html = ""
    for i in range(1, 6):
        if i <= int(rating):
            html += '<i class="fa-solid fa-star choose-star"></i>'
        else:
            html += '<i class="fa-solid fa-star blank-star"></i>'
    return mark_safe(html)