# coding: utf-8
from decorators import check_login, render_to
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from forms import AccountForm
from models import Account


@render_to('security/index.html')
def login(request):
    data = {}
    if request.POST:
        form = AccountForm(request.POST)
        if form.is_valid():
            try:
                acc = Account.objects.get(
                        phone_number=form.cleaned_data['phone_number'],
                        pin_code=form.cleaned_data['pin_code'])
            except Account.DoesNotExist:
                msg = 'Утасны дугаар эсвэл Нууц үг буруу байна'
                form._errors["phone_number"] = form.error_class([msg])
            else:
                request.session['account_id'] = acc.id
                return redirect(reverse('game.views.select_cell'))

    else:
        form = AccountForm()

    data['form'] = form
    return data


@check_login
def logout(request):
    del request.session['account_id']
    return redirect(reverse('public.views.index'))
