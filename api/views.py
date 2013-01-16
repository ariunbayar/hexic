from api.models import Sms
from security.models import Account
from helpers import generate_password, is_deposit
from django.http import HttpResponse


def new_msg(request):
    sms = Sms()

    sender = request.GET['phone']
    msg = request.GET['msg']

    sms.sender = sender
    sms.text = msg
    if not (sender and msg):
        return HttpResponse('404.html')

    phone, credit = is_deposit(sender, msg)
    if not (phone and credit):
        return HttpResponse('404.html')

    try:
        old_acc = Account.objects.get(phone_number=phone)
    except Account.DoesNotExist:
        random_number = generate_password()
        new_acc = Account()

        new_acc.phone_number = phone
        new_acc.pin_code = random_number
        new_acc.credit = credit

        new_acc.save()

        sms.account = new_acc
        sms.action = Sms.NEW_ACC
    else:
        old_acc.credit += credit
        old_acc.save()

        sms.account = old_acc
        sms.action = Sms.DEPOSIT

    sms.save()
    return HttpResponse('msg received')
