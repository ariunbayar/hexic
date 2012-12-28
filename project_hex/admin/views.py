# coding: utf-8
import time
from hashlib import sha1

from flask import request, flash, abort, current_app
import db
from helpers import template, redirect, cache_get, query_db
from . import admin
from .forms import UserForm
from user.decorators import login_required
from user.models import User
from user.newmodel import User as NewUser


@admin.route("/")
@login_required
def dashboard(user):
    keys = cache_get(current_app.config['MEMCACHE_KEYS']) or []
    cxt = {
        "user_count": User.query.count(),
        "cache_count": len(keys),
        "users": NewUser.query(phone='99437911'),
    }
    return template("admin/dashboard.html", user=user, **cxt)


@admin.route("/users/")
@login_required
def users(user):
    users = User.get_all()
    return template("admin/users.html", user=user, users=users)


@admin.route("/user/add/", methods=['POST', 'GET'])
@login_required
def user_add(user):
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        values = form.data
        if not values['name']:
            hash_str = "%s%s" % (values['phone'], time.time())
            values['name'] = "Тоглогч %s" % sha1(hash_str).hexdigest()[:8]
        user = User(name=values['name'],
                    email=values['email'],
                    phone=values['phone'],
                    code=values['code'])
        db.session.add(user)
        db.session.commit()
        flash(u"Шинэ хэрэглэгчийг амжилттай нэмлээ", "success")
        return redirect("admin.users")
    return template("admin/user_edit.html", user=user, form=form)


def get_user_or_404(uid):
    user = User.get_user(uid)
    if not isinstance(user, User):
        abort(404)
    return user


@admin.route("/user/edit/<int:uid>", methods=['POST', 'GET'])
@login_required
def user_edit(user, uid):
    edit_user = get_user_or_404(uid)

    if request.method == "POST":
        form = UserForm(request.form)
        form.uid = edit_user.id
        if form.validate():
            form.populate_obj(edit_user)
            db.session.add(edit_user)
            db.session.commit()
            flash(u"Өөрчлөлт хадгалагдлаа", "success")
            return redirect("admin.users")
    else:
        form = UserForm(name=edit_user.name, email=edit_user.email,
                        phone=edit_user.phone, code=edit_user.code)
    return template("admin/user_edit.html", user=user, form=form)


@admin.route("/cache/")
@login_required
def cache(user):
    cache = current_app.cache
    items = cache.get(current_app.config['MEMCACHE_KEYS']) or []
    items = sorted(items)
    hit_ratios = [cache.get('hit_ratio_%s' % item) for item in items]
    return template("admin/cache.html", user=user, items=items,
                    hit_ratios=hit_ratios)


@admin.route("/cache/clear/")
@login_required
def cache_clear(user):
    current_app.cache.clear()
    flash(u"Амжилттай цэвэрлэлээ", "success")
    return redirect("admin.cache")


@admin.route("/cache/show/<string:key>/")
@login_required
def cache_show(user, key):
    item = cache_get(key)
    return template("admin/cache_show.html", user=user, item=item)
