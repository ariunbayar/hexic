from api.models import Sms
from security.models import Account
from helpers import generate_password, is_deposit
from django.http import HttpResponse, Http404


def new_msg(request):
    sender = request.GET['phone']
    msg = request.GET['msg']

    if not sender:
        raise Http404

    sms = Sms()
    sms.sender = sender
    sms.text = msg

    phone, credit = is_deposit(sender, msg)
    if phone and credit:
        try:
            old_acc = Account.objects.get(phone_number=phone)
        except Account.DoesNotExist: # Adding new account
            random_number = generate_password()
            new_acc = Account()

            new_acc.phone_number = phone
            new_acc.pin_code = random_number
            new_acc.credit = credit

            new_acc.save()

            sms.account = new_acc
            sms.action = Sms.NEW_ACC
        else: # Adding credit for old account
            old_acc.credit += credit
            old_acc.save()

            sms.account = old_acc
            sms.action = Sms.DEPOSIT

    sms.save()
    return HttpResponse('msg received')
