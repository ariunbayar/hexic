import json

from api.models import Sms
from decorators import ajax_required, api_key_valid
from helpers import generate_password, is_deposit
from security.models import Account
from settings import SMS_CLIENT_KEY

from django.contrib.sessions.models import Session
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


def message_received(request):
    sender = request.GET.get('phone')
    msg = request.GET.get('msg')
    client_key = request.GET.get('key')

    if (not sender) or (client_key != SMS_CLIENT_KEY):
        raise Http404

    sms = Sms()
    sms.sender = sender
    sms.text = msg

    phone, credit = is_deposit(sender, msg)
    if phone and credit:
        try:
            old_acc = Account.objects.get(phone_number=phone)
        except Account.DoesNotExist:  # Adding new account
            random_number = generate_password()
            new_acc = Account()

            new_acc.phone_number = phone
            new_acc.pin_code = random_number
            new_acc.credit = credit

            new_acc.save()

            sms.account = new_acc
            sms.action = Sms.NEW_ACC
        else:  # Adding credit for old account
            old_acc.credit += credit
            old_acc.save()

            sms.account = old_acc
            sms.action = Sms.DEPOSIT

    sms.save()
    return HttpResponse('msg received')


def _get_account_id_by_session(session_id):
    session = Session.objects.get(session_key=session_id)
    return session.get_decoded().get('account_id')


@csrf_exempt
@require_POST
@ajax_required
@api_key_valid
def game_server(request):
    game_data = json.loads(request.body)

    winner_id = _get_account_id_by_session(game_data['winner'])
    account_ids = map(lambda sid: _get_account_id_by_session(sid), game_data['players'])
    import pprint; pprint.pprint((account_ids, winner_id))

    return HttpResponse('ACK')
