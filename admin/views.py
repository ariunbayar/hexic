# coding: utf-8
from admin.decorators import check_login
from admin.helpers import ShortPaginator, search
from admin.models import Admin
from admin.forms import AdminLoginForm
from api.models import Sms
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response, redirect
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
    data['accounts'] = Account.objects.all()
    paginator = Paginator(data['accounts'], 20)
    data['paginator'] = paginator

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

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
    data['admins'] = Admin.objects.all()

    paginator = Paginator(data['admins'], 20)
    data['paginator'] = paginator

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

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
    data['messages'] = Sms.objects.all()

    if 'search_val' in request.GET and request.GET['search_val']:
        data['messages'] = search(request.GET['search_val'])

    if 'filter_by' in request.GET:
        filter_by = request.GET['filter_by']
        data['messages'] = Sms.objects.filter(action=filter_by)

    data['admin_id'] = request.session['admin_id']
    data['messages'] = data['messages'].order_by('-date_time')
    paginator = ShortPaginator(data['messages'], 20)
    data['paginator'] = paginator

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        data['page'] = paginator.page(page)
    except (EmptyPage, InvalidPage):
        data['page'] = paginator.page(paginator.num_pages)

    return render_to_response("admin/messages.html", data,
                                context_instance=RequestContext(request))
