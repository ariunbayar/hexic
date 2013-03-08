from functools import wraps

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def login_required(f):
    @wraps(f)
    def decorated_function(r, *args, **kwargs):
        if not r.session.get('id'):
            return HttpResponseRedirect(reverse('login'))
        return f(r, *args, **kwargs)
    return decorated_function
