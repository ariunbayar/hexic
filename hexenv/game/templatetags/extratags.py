from django.template import Library, TemplateSyntaxError, Node

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

