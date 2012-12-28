from random import randint as rand

from django.contrib.messages import add_message, SUCCESS as MSG_SUCCESS
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, defaultfilters as filters
#from django.utils import simplejson as json

from admin.forms import PlayerForm, BoardForm
from game.models import Board
from player.models import Player


def board_show(request, name):
    ctx = {'name': name}
    return render_to_response('admin/board_show.html',
            RequestContext(request, ctx))


def board_new(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save()
            add_message(request, MSG_SUCCESS,
                        'New board "%s" saved!' % board.name)
            return HttpResponseRedirect(reverse('admin-board-show',
                                                args=[board.name]))
    else:
        form = BoardForm()
    ctx = {'form': form, 'range': range(10)}
    return render_to_response('admin/board_new.html',
            RequestContext(request, ctx))


def show_moves(request):
    return render_to_response('admin/show_moves.html', {})


def dashboard(request):
    players = Player.objects.all()
    boards = Board.objects.all()
    ctx = {'players': players, 'boards': boards}
    return render_to_response('admin/dashboard.html',
            RequestContext(request, ctx))


def player_show(request, player_id):
    player = Player.objects.get(pk=player_id)
    cxt = {'player': player}
    return render_to_response('admin/player_show.html',
            RequestContext(request, cxt))


def player_new(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save()
            add_message(request, MSG_SUCCESS, 'New player saved!')
            return HttpResponseRedirect(reverse('admin-player-show',
                                                args=[player.id]))
    else:
        form = PlayerForm()

    cxt = {'form': form}
    return render_to_response('admin/player_new.html',
            RequestContext(request, cxt))


def player_edit(request, player_id):
    player = Player.objects.get(pk=player_id)
    if request.method == 'POST':
        form = PlayerForm(request.POST, instance=player)
        if form.is_valid():
            player = form.save()
            add_message(request, MSG_SUCCESS, 'Changes saved!')
            return HttpResponseRedirect(reverse('admin-player-show',
                                                args=[player.id]))
    else:
        form = PlayerForm(instance=player)

    cxt = {'form': form}
    return render_to_response('admin/player_edit.html',
            RequestContext(request, cxt))
