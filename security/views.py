# coding: utf-8
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from models import Account
from forms import AccountForm


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
                request.session['account_id'] = acc
                return redirect(reverse('game.views.board'))

    else:
        form = AccountForm()

    data['form'] = form
    return render_to_response("security/index.html", data,
                                context_instance=RequestContext(request))


def logout(request):
    del request.session['account_id']
    return redirect(reverse('public.views.index'))
