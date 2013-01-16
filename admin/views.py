# coding: utf-8
from admin.decorators import check_login
from admin.models import Admin
from admin.forms import AdminLoginForm
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from security.models import Account


def login(request):
    data = {}
    if request.POST:
        form = AdminLoginForm(request.POST)
        import logging
        logging.error(form.is_valid())
        if form.is_valid():
            try:
                admin = Admin.objects.get(
                        user_name=form.cleaned_data['user_name'],
                        password=form.cleaned_data['password'])
            except Admin.DoesNotExist:
                msg = 'Нэр эсвэл Нууц үг буруу байна'
                form._errors["user_name"] = form.error_class([msg])
            else:
                request.session['admin_id'] = admin.id
                data['admin_id'] = request.session['admin_id']
                return redirect(reverse('admin.views.accounts'))

    else:
        form = AdminLoginForm()

    data['form'] = form
    return render_to_response("admin/login.html", data,
                                context_instance=RequestContext(request))


@check_login
def logout(request):
    del request.session['admin_id']
    return redirect(reverse('admin.views.login'))


@check_login
def accounts(request):
    data = {}
    data['accounts'] = Account.objects.all()
    data['admin_id'] = request.session['admin_id']
    return render_to_response("admin/accounts.html", data,
                                context_instance=RequestContext(request))


@check_login
def admins(request):
    data = {}
    data['admins'] = Admin.objects.all()
    data['admin_id'] = request.session['admin_id']
    return render_to_response("admin/admins.html", data,
                                context_instance=RequestContext(request))
