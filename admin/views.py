# coding: utf-8
from admin.decorators import check_login
from admin.helpers import ShortPaginator
from admin.models import Admin
from admin.forms import AdminLoginForm, AccountForm
from api.models import Sms
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import Http404
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from security.models import Account


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
                messages.add_message(request, messages.INFO, 'Hello world!!!')
                msg = 'Нэр эсвэл Нууц үг буруу байна'
                form._errors["user_name"] = form.error_class([msg])
            else:
                request.session['admin_id'] = admin.id
                data['admin_id'] = request.session['admin_id']
                return redirect(reverse('admin.views.accounts'))

    else:
        if 'admin_id' in request.session:
            return redirect(reverse('admin.views.accounts'))

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
    qs = Account.objects.all()
    paginator = Paginator(qs, 20)
    data['paginator'] = paginator

    page = request.GET['page'] if 'page' in request.GET else 1
    try:
        data['page'] = paginator.page(page)
    except (EmptyPage, InvalidPage):
        data['page'] = paginator.page(paginator.num_pages)

    data['admin_id'] = request.session['admin_id']
    return render_to_response("admin/accounts.html", data,
                                context_instance=RequestContext(request))


@check_login
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

    data['admin_id'] = request.session['admin_id']
    return render_to_response("admin/admins.html", data,
                                context_instance=RequestContext(request))


@check_login
def messages(request):
    data = {}
    param = request.GET

    # filter objects
    qs = Sms.objects.all()
    if 'sender' in param and param['sender']:
        qs = qs.filter(sender__startswith=param['sender'])
    if 'phone' in param and param['phone']:
        qs = qs.filter(account__phone_number__startswith=int(param['phone']))
    if 'action' in param:
        if 'deposit' == param['action']:
            qs = qs.filter(action=Sms.DEPOSIT)
        if 'new_acc' == param['action']:
            qs = qs.filter(action=Sms.NEW_ACC)
        if 'none' == param['action']:
            qs = qs.filter(action=Sms.NONE)
    qs = qs.order_by('-date_time')

    # pagination
    data['paginator'] = paginator = ShortPaginator(qs, 20)
    page = param['page'] if 'page' in param else 1

    try:
        data['page'] = paginator.page(int(page))
    except (EmptyPage, InvalidPage):
        data['page'] = paginator.page(paginator.num_pages)  # last page

    # admin login indicator
    data['admin_id'] = request.session['admin_id']

    return render_to_response("admin/messages.html", data,
                                context_instance=RequestContext(request))


@check_login
def add_acc(request):
    data = {}
    if request.POST:
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('admin.views.accounts'))

    else:
        form = AccountForm()

    data['admin_id'] = request.session['admin_id']

    data['form'] = form
    return render_to_response('admin/account_form.html', data,
                                context_instance=RequestContext(request))


@check_login
def update_acc(request):
    data = {}
    if request.POST:
        form = AccountForm(request.POST)
        if form.is_valid():
            if 'acc_id' in form.cleaned_data:
                acc = get_object_or_404(Account, pk=form.cleaned_data['acc_id'])
                acc.phone_number = form.cleaned_data['phone_number']
                acc.pin_code = form.cleaned_data['pin_code']
                acc.credit = form.cleaned_data['credit']
                acc.save()
            else:
                raise Http404

        return redirect(reverse('admin.views.accounts'))

    else:
        form = AccountForm()
        if 'acc_id' in request.GET and request.GET['acc_id']:
            acc_id = request.GET['acc_id']
            acc = get_object_or_404(Account, pk=acc_id)
            form = AccountForm(initial={
                                'phone_number': acc.phone_number,
                                'pin_code': acc.pin_code,
                                'credit': acc.credit,
                                'acc_id': acc_id})
        data['form'] = form

    data['acc_id'] = acc_id
    data['admin_id'] = request.session['admin_id']
    return render_to_response('admin/account_form.html', data,
                                context_instance=RequestContext(request))


@check_login
def del_acc(request):
    if 'acc_id' in request.GET:
        acc = get_object_or_404(Account, pk=request.GET['acc_id'])
        acc.delete()

    return redirect(reverse('admin.views.accounts'))


