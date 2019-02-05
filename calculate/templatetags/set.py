from django import template

from calculate.models import ActivSet

register = template.Library()

@register.simple_tag
def hi(a):
    sets = ActivSet.objects.filter(user_id=a).count()

    return sets

