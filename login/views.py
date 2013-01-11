# coding: utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Account
from forms import AccountForm

def index(request):
    data_dict = {}
    if request.POST:
        form = AccountForm(request.POST)
        if form.is_valid():
            try:
                Account.objects.get(
                        phone_number=form.cleaned_data['phone_number'],
                        pin_code=form.cleaned_data['pin_code'])
            except Account.DoesNotExist:
                msg = 'Утасны дугаар эсвэл Нууц үг буруу байна'
                form._errors["phone_number"] = form.error_class([msg])
            else:
                return render_to_response("hexic/animation.html")

    else:
        form = AccountForm()

    data_dict['form'] = form
    return render_to_response("login/index.html",
                                data_dict,
                                context_instance=RequestContext(request))
