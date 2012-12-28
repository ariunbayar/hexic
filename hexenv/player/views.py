from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from player.forms import LoginForm
from player.decorators import login_required


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['id'] = form.instance.id
            return HttpResponseRedirect(reverse('homepage'))
    else:
        form = LoginForm()

    cxt = {'form': form}
    return render_to_response('player/login.html',
            RequestContext(request, cxt))


@login_required
def logout(request):
    del request.session['id']
    return HttpResponseRedirect(reverse('homepage'))
