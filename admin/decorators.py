from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from functools import wraps


def check_login(function):
    def check(request, *args, **kwargs):
        if 'admin_id' in request.session:
            import logging
            logging.error(args)
            logging.error(kwargs)
            return function(request, *args, **kwargs)
        else:
            return redirect(reverse('admin.views.login'))
    return wraps(function)(check)
