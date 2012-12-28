# coding: utf-8
from datetime import datetime
from flask import request, session, flash
from helpers import template, redirect
from . import user
from .decorators import login_required
from .forms import LoginForm
from .models import User


@user.route("/login/", methods=['POST', 'GET'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        data = form.data
        user = User.query.filter(User.phone == data['phone']).first()
        if user and str(user.code) == data['code']:
            session['uid'] = user.id
            return redirect("user.profile")
        else:
            form.phone.errors.append(u"Дугаар, код буруу байна")

    cxt = {'form': form}
    return template("user/login.html", **cxt)


@user.route("/logout/")
@login_required
def logout(user):
    session.pop("uid", None)
    return redirect('home.index')


@user.route("/profile/")
@login_required
def profile(user):
    return template("user/profile.html", user=user, title=u"профайл")


@user.route("/login-as-guest/")
def login_guest():
    # TODO
    flash(u"Одоогоор зочноор нэвтрэх боломжгүй байна", "warning")
    return redirect("user.login")


@user.route("/welcome/")
@login_required
def welcome(user):
    user.last_seen = datetime.now()
    user.save()
    return template("user/welcome.html", user=user)
