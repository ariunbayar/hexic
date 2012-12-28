from functools import wraps

from django.contrib.messages import add_message, WARNING as MSG_WARNING
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def login_required(f):
    @wraps(f)
    def decorated_function(r, *args, **kwargs):
        if not r.session.get('id'):
            add_message(r, MSG_WARNING, 'Please log in!')
            return HttpResponseRedirect(reverse('login'))
        return f(r, *args, **kwargs)
    return decorated_function
