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
def get_id__url(value):
    mo = re.match("/(en|es)/(.+/|.+/\d+/)", value)

    if mo:
        result = mo.group(2)
    else:
        result = ""

    return result

@register.filter
def get_i_item(value, arg):
    return value[int(arg)]


@register.filter
def get_image_url(value):
    mo = re.match(".+(http://.+\.jpg).+", value)

    print mo.group(1)
    if mo:
        result = mo.group(1)
    else:
        result = ""

    return result


@register.filter
def get_local_id(value):
    return Local.objects.get(nombre__iexact=value).id


@register.filter
def is_equal_with(value,arg):
    if str(value) == str(arg):
        return True
    return False

