from django import template
from mainapp.models import Category

register = template.Library()


@register.inclusion_tag('mainapp/list_cats.html')
def show_all_cats():
    return {"cats": Category.objects.all()}
