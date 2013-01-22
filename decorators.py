from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from functools import wraps


def check_login(function):
    def check(request, *args, **kwargs):
        if 'account_id' in request.session:
            return function(request, *args, **kwargs)
        else:
            return redirect(reverse('security.views.login'))
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
