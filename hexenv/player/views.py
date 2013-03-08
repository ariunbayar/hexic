from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _

from player.forms import LoginForm
from player.decorators import login_required
from player.models import Player


DESIGNS = xrange(1, 16)


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            player = form.object
            request.session['id'] = player.id
            return HttpResponseRedirect(reverse('homepage'))
    else:
        form = LoginForm()
    cxt = RequestContext(request, {'form': form})
    return render_to_response('player/login.html', cxt)


@login_required
def logout(request):
    del request.session['id']
    return HttpResponseRedirect(reverse('homepage'))


@login_required
def settings(request):
    player = get_object_or_404(Player, pk=request.session['id'])
    
    if 'design' in request.GET:
        design = int(request.GET.get('design'))
        if design in DESIGNS:
            player.design = design
            player.save()
    cxt = RequestContext(request, {'designs': DESIGNS, 'player': player})
    return render_to_response('player/settings.html', cxt)
            

