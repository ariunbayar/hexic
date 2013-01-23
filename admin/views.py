# coding: utf-8
from admin.decorators import check_login
from admin.helpers import ShortPaginator
from admin.models import Admin
from admin.forms import AdminLoginForm, AccountForm, AdminForm
from api.models import Sms
from hexic.decorators import render_to
from security.models import Account

from django.contrib import messages as flash
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import redirect, get_object_or_404


@render_to("admin/login.html")
def login(request):
    data = {}
    if request.POST:
        form = AdminLoginForm(request.POST)
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
                return redirect(reverse('admin.views.accounts'))

    else:
        if 'admin_id' in request.session:
            return redirect(reverse('admin.views.accounts'))

        form = AdminLoginForm()

    data['form'] = form
    return data


@check_login
def logout(request):
    del request.session['admin_id']
    return redirect(reverse('admin.views.login'))


@check_login
@render_to("admin/accounts.html")
def accounts(request):
    data = {}
    qs = Account.objects.all()
    paginator = Paginator(qs, 20)
    data['paginator'] = paginator

    page = request.GET['page'] if 'page' in request.GET else 1
    try:
        data['page'] = paginator.page(page)
    except (EmptyPage, InvalidPage):
        data['page'] = paginator.page(paginator.num_pages)

    return data


@check_login
@render_to("admin/admins.html")
def admins(request):
    data = {}
    qs = Admin.objects.all()

    paginator = Paginator(qs, 20)
    data['paginator'] = paginator

    page = request.GET['page'] if 'page' in request.GET else 1
    try:
        data['page'] = paginator.page(page)
    except (EmptyPage, InvalidPage):
        data['page'] = paginator.page(paginator.num_pages)

    return data


@check_login
@render_to("admin/messages.html")
def messages(request):
    data = {}
    param = request.GET

    # filter objects
    qs = Sms.objects.all()
    if 'sender' in param and param['sender']:
        qs = qs.filter(sender__startswith=param['sender'])
        data['sender'] = param['sender']
    if 'phone' in param and param['phone']:
        qs = qs.filter(account__phone_number__startswith=int(param['phone']))
        data['phone'] = param['phone']
    if 'action' in param:
        if 'deposit' == param['action']:
            qs = qs.filter(action=Sms.DEPOSIT)
            data['deposit'] = param['action']
        if 'new_acc' == param['action']:
            qs = qs.filter(action=Sms.NEW_ACC)
            data['new_acc'] = param['action']
        if 'none' == param['action']:
            qs = qs.filter(action=Sms.NONE)
            data['none'] = param['action']
    qs = qs.order_by('-date_time')

    # pagination
    data['paginator'] = paginator = ShortPaginator(qs, 20)
    page = param['page'] if 'page' in param else 1

    try:
        data['page'] = paginator.page(int(page))
    except (EmptyPage, InvalidPage):
        data['page'] = paginator.page(paginator.num_pages)  # last page

    return data


@check_login
@render_to('admin/account_form.html')
def add_acc(request):
    data = {}
    if request.POST:
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            flash.add_message(request, flash.SUCCESS, 'Account added')
            return redirect(reverse('admin.views.accounts'))

    else:
        form = AccountForm()

    data['form'] = form
    return data


@check_login
@render_to('admin/account_form.html')
def update_acc(request, acc_id):
    data = {}
    acc = get_object_or_404(Account, pk=acc_id)

    if request.POST:
        form = AccountForm(request.POST, instance=acc)
        if form.is_valid():
            form.save()
            flash.add_message(request, flash.SUCCESS, 'Account updated')
            return redirect(reverse('admin.views.accounts'))

    else:
        form = AccountForm(instance=acc)
    data['form'] = form
    return data


@check_login
def del_acc(request, acc_id):
    acc = get_object_or_404(Account, pk=acc_id)
    acc.delete()
    flash.add_message(request, flash.SUCCESS, 'Account deleted')

    return redirect(reverse('admin.views.accounts'))


@check_login
@render_to('admin/admin_form.html')
def add_admin(request):
    data = {}

    if request.POST:
        form = AdminForm(request.POST)
        if form.is_valid():
            form.save()
            flash.add_message(request, flash.SUCCESS, 'Admin added')
            return redirect(reverse('admin.views.admins'))
    else:
        form = AdminForm()

    data['form'] = form
    return data


@check_login
@render_to('admin/admin_form.html')
def update_admin(request, admin_id):
    data = {}
    admin = get_object_or_404(Admin, pk=admin_id)

    if request.POST:
        form = AdminForm(request.POST, instance=admin)
        if form.is_valid():
            form.save()
            flash.add_message(request, flash.SUCCESS, 'Admin updated')
            return redirect(reverse('admin.views.admins'))
    else:
        form = AdminForm(instance=admin)

    data['form'] = form
    return data


@check_login
def del_admin(request, admin_id):
    admin = get_object_or_404(Admin, pk=admin_id)
    admin.delete()
    flash.add_message(request, flash.SUCCESS, 'Admin deleted')

    return redirect(reverse('admin.views.admins'))
