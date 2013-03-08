from django.template import Library

register = Library()

@register.filter
def mult(value, arg):
    return value * arg;

@register.simple_tag
def multEvenAdd(val, mul1, mul2, add):
    rval = mul1 * mul2
    if val % 2 == 0:
        rval += add
    return rval

@register.filter
def odd(val, s):
    return s if val % 2 else ""

@register.filter
def even(val, s):
    return s if not val % 2 else ""

@register.simple_tag
def array_get(arr, a, b, c):
    return arr[a][b][c]
