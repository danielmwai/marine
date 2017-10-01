"""User group checker."""
from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    """Method to get the user group."""
    try:
        group = Group.objects.get(name=group_name)
        return group in user.groups.all()
    except Exception:
        return False


@register.filter(name='gen_value')
def gen_value(value, args):
    """Method to translater keys to actual names."""
    if value in args:
        return args[value]
    else:
        return value
