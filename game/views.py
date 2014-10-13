# coding: utf-8
import json
import hashlib
import redis
from decorators import render_to, check_login
from django.http import HttpResponse
from django.core.urlresolvers import reverse

from security.models import Account
from utils import memval
from settings import SIO_URL


@check_login
@render_to("game/dashboard.html")
def dashboard(request):
    return {}


@check_login
def quick_match(request):
    # TODO fix the race condition
    pending_users = memval('pending_users') or []
    matched_users = memval('matched_users') or {}
    user_id = request.session.get('account_id')

    if user_id in matched_users:
        # opponent has been chosen
        opponent_id = matched_users[user_id]
    elif pending_users:
        # match to this opponent
        is_found = False
        for idx, opponent_id in enumerate(pending_users):
            if opponent_id != user_id:
                matched_users[opponent_id] = user_id
                matched_users[user_id] = opponent_id
                is_found = True
                pending_users.pop(idx)
                break
        if not is_found:
            opponent_id = None
    else:
        # user should wait for others
        pending_users.append(user_id)
        opponent_id = None

    memval('pending_users', pending_users)
    memval('matched_users', matched_users)

    values = dict()
    values['opponent_id'] = opponent_id
    if opponent_id:
        match_str = 'vs'.join(sorted([str(user_id), str(opponent_id)]))
        match_key = hashlib.md5(match_str).hexdigest()[:8]
        url = reverse('game.views.play')
        values['redirect_url'] = '%s?key=%s' % (url, match_key)

    return HttpResponse(json.dumps(values), content_type="application/json")


def auto_login(request):  # TODO debug only
    if not request.session.exists(request.session.session_key):
        request.session.create()
    session_id = request.session.session_key
    reserved_users = memval('reserved_users') or {}

    if session_id in reserved_users:
        qs = Account.objects.filter(pk=reserved_users[session_id])
    elif reserved_users:
        qs = Account.objects.exclude(id__in=reserved_users.values())
    else:
        qs = Account.objects.all()

    try:
        user = qs[:1].get()
        reserved_users[session_id] = user.id
        memval('reserved_users', reserved_users)
        rval = dict(phone_number=user.phone_number,
                    pin_code=user.pin_code)
    except Exception:
        rval = None

    return HttpResponse(json.dumps(rval), content_type="application/json")


@check_login
@render_to('game/play.html')
def play(request):
    # remove from match making
    matched_users = memval('matched_users') or {}
    user_id = request.session.get('account_id')
    if user_id in matched_users:
        del matched_users[user_id]
        memval('matched_users', matched_users)

    # remove if these players used to play
    redis_cache = redis.StrictRedis()
    redis_cache.delete('game_%s' % request.GET.get('key'))

    ctx = dict(
        match_key=request.GET.get('key'),
        sio_url=SIO_URL
    )
    return ctx
