from security.models import Account
from helpers import generate_password, is_deposit
from django.core.urlresolvers import reverse
from django.shortcuts import redirect


def new_msg(request):
    sender = request.GET['phone']
    msg = request.GET['msg']

    if sender and msg:
        phone, credit = is_deposit(sender, msg)
        if phone and credit:
            try:
                old_acc = Account.objects.get(phone_number=phone)
            except Account.DoesNotExist:
                random_number = generate_password()
                new_acc = Account()

                new_acc.phone_number=phone
                new_acc.pin_code=random_number
                new_acc.credit=credit

                new_acc.save()
            else:
                old_acc.credit += credit
                old_acc.save()

    return redirect(reverse('public.views.index'))
