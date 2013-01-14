from django.shortcuts import render_to_response
from django.template import RequestContext
from decorators import check_login


@check_login
def board(request):
    data = {}
    data['account_id'] = request.session['account_id']
    return render_to_response("game/animation.html", data,
                               context_instance=RequestContext(request))
