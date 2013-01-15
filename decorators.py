from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from functools import wraps


def check_login(function):
    def check(request, *args, **kwargs):
        if 'account_id' in request.session:
            return function(request, *args, **kwargs)
        else:
            return redirect(reverse('security.views.login'))
    return wraps(function)(check)
