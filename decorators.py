from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from functools import wraps

from settings import SMS_CLIENT_KEY


def check_login(function):
    def check(request, *args, **kwargs):
        if 'account_id' in request.session:
            return function(request, *args, **kwargs)
        else:
            return redirect(reverse('security.views.login'))
    return wraps(function)(check)


def check_admin(function):
    def check(request, *args, **kwargs):
        if 'admin_id' in request.session:
            return function(request, *args, **kwargs)
        else:
            return redirect(reverse('admin.views.login'))
    return wraps(function)(check)


def render_to(template=None, mimetype=None):
    def renderer(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):
            output = function(request, *args, **kwargs)
            if not isinstance(output, dict):
                return output
            tmpl = output.pop('TEMPLATE', template)
            return render_to_response(tmpl, output, \
                context_instance=RequestContext(request), mimetype=mimetype)
        return wrapper
    return renderer


def ajax_required(f):
    """
    AJAX request required decorator
    use it in your views:

    @ajax_required
    def my_view(request):
        ....

    """
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def api_key_valid(f):
    def wrap(request, *args, **kwargs):
        if request.GET.get('key') != SMS_CLIENT_KEY:
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)
    return wrap
