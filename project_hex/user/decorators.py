# coding: utf-8
from datetime import datetime
from functools import wraps
from flask import session, redirect, url_for, flash, request, current_app
from .newmodel import User


def login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        user = User.query(id=session.get('uid', None)).get()
        if not isinstance(user, User):
            flash(u"Сайтад нэвтрээгүй байна", "warning")
            return redirect(url_for("user.login"))
        # allow to welcome and logout
        skip = str(request.url_rule) == "/welcome/" or \
               str(request.url_rule) == "/logout/"
        if not skip:
            if user.last_seen is None:  # show welcome if user has never accessed
                return redirect(url_for("user.welcome"))
            # update last_seen
            expiry = datetime.now() - current_app.config['LAST_SEEN_INTERVAL']
            if user.last_seen < expiry:
                user.last_seen = datetime.now()
                user.cache_update()

        kwargs['user'] = user
        return f(*args, **kwargs)
    return decorator
