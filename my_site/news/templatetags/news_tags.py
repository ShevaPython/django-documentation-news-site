from django import template
from django.db.models import Count,F

from news.models import Category

register = template.Library()


# @register.simple_tag(name='get_cat')
# def get_categories():
#     return Category.objects.all()


@register.inclusion_tag('news/list_category.html',name='show_cat')
def show_categories():
    # categories = Category.objects.all()
    categories=Category.objects.annotate(col=Count('news',filter=F('news__is_publish'))).filter(col__gt=0)
    return {'categories': categories}
