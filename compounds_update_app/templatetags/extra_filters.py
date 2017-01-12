# -*- coding: utf-8 -*-

from django import template
import re

from reactivos_sst_app.models import Local

register = template.Library()


@register.filter
def concat_str(value, arg):
    return "%s%s" % (arg, value)


@register.filter
def truncatechars(value, arg):
    count = 0
    result = ""

    cant = int(arg)

    for char in value:
        if count < cant:
            result += char
        else:
            break

        count += 1

    result += " ..."
    return result


@register.filter
def contains(value, arg):
    nombre = unicode(arg)
    for obj in value:
        if nombre == obj.persona.nombre:
            return True

    return False


@register.filter
def get_i_item(value, arg):
    return value[int(arg)]


@register.filter
def get_local_id(value):
    return Local.objects.get(nombre__iexact=value).id


@register.filter
def is_equal_with(value, arg):
    if str(value) == str(arg):
        return True
    return False


@register.filter
def is_li_than(value, arg):
    if int(value) >= int(arg):
        return True
    return False


@register.filter
def is_si_than(value, arg):
    if int(value) <= int(arg):
        return True
    return False


@register.filter
def is_lg_than(value, arg):
    if int(value) > int(arg):
        return True
    return False


@register.filter
def is_sm_than(value, arg):
    if int(value) < int(arg):
        return True
    return False


@register.filter
def get_management_form(value):
    return value.management_form


@register.filter
def get_formset_id(value):
    return value.id


@register.filter
def get_empty_form_as(value):
    return value.empty_form.as_table
