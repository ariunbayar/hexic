# coding: utf-8
from decorators import render_to, check_login
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render_to_response
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from game.models import Board
from game.forms import NewBoardForm
from security.models import Account
from django.conf import settings
from utils import (memval, move_valid, game_start,
                   random_cell, with_cells)
from django.db.models import Q


@check_login
@render_to('game/play.html')
def play(request):
    user_id = str(request.session.get('account_id'))
    account = Account.objects.get(pk=user_id)
    board_id = request.GET.get('board_id', None)

    working_boards = Board.objects.filter(~Q(status=Board.STATUS_ERROR))
    try:
        working_board = working_boards.get(pk=board_id)
    except ObjectDoesNotExist:
        return Http404

    if board_id:
        board = memval('board_%s' % board_id)
        ctx = {
            'user_id': int(user_id),
            'update_interval': settings.UPDATE_INTERVAL,
            'waiting_board': working_board,
        }

    board = memval('board_%s' % board_id)
    users = memval('%s_board_users' % board_id)
    user_ids = working_board.players.split(',')

    if working_board.status == Board.STATUS_IN_PROGRESS:
        if user_id not in user_ids:
           return render_to_response('game/notification.html')

    if not with_cells(users, account):
        # Automatically select cell if cell not selected

        if user_id not in user_ids:
            user_ids.append(user_id)
            if len(user_ids) == 2:
                default_bytes = 20
                for user_id in user_ids:
                    y, x = random_cell(board, users)
                    board[y][x] = default_bytes - board[y][x]
                    users[y][x] = [int(user_id), '#FF0000']

                memval('board_%s' % board_id, board)
                memval('%s_board_users' % board_id, users)
                working_board.status = Board.STATUS_IN_PROGRESS
                working_board.players = ','.join(user_ids)
                working_board.save()

    return ctx

@check_login
@render_to("game/dashboard.html")
def dashboard(request):
    # TODO include number of players of one board
    count_players = 2
    user_id = request.session.get('account_id')
    board_players = [user_id]
    for i in xrange(count_players):
        board_players.append(0)
    if request.POST:
        form = NewBoardForm(request.POST)
        if form.is_valid():
            user_id = request.session.get('account_id')
            board = Board(
                    name=form.cleaned_data['name'],
                    status=Board.STATUS_WAIT,
                    players=str(user_id))
            board.save()

            board_id = board.id
            game_start(board_id)
            return redirect(reverse('game.views.play') + '?board_id=%s' % board_id)
    else:
        form = NewBoardForm()

    ctx = {
        'active_boards': Board.objects.filter(status=Board.STATUS_WAIT),
        'form': form}
    return ctx


@check_login
def select_board(request):
    users = []
    board_id = request.GET.get('board_id')
    user_id = request.session.get('account_id')
    board = Board.objects.get(board_id)
    indx = board.players.index(0) if 0 in board.players else None
    if indx:
        board.players[indx] = user_id
        board.save()
        if not 0 in board.players:
            board.status = Board.STATUS_IN_PROGRESS
            board.save()
            game_start(board.id)
            return redirect(reverse('game.views.play') + '?board_id=%s' % board.id)

    qs = Account.objects.filter(pk__in=board.players)
    for account in qs:
        users.append(account.phone_number)
    val = simplejson.dumps({'users': users})
    return HttpResponse(val, mimetype="application/json")


@check_login
def progress(request):
    """ dumps game progress in json """
    board_id = request.GET.get('board_id')
    board = memval('board_%s' % board_id)
    board_users = memval('%s_board_users' % board_id)
    simple_moves = memval('%s_simple_moves' % board_id)
    val = simplejson.dumps({'moves': simple_moves, board_id: board,
                            'board_id': board_id, 'board_users': board_users})
    return HttpResponse(val, mimetype="application/json")


@check_login
def move(request):
    """ adds the move to move list """
    ax = request.GET['fx'];
    ay = request.GET['fy'];
    bx = request.GET['tx'];
    by = request.GET['ty'];
    move = (int(ax), int(ay), int(bx), int(by))
    user_id = int(request.session.get('account_id'));

    board_id = request.GET.get('board_id')
    queue = memval('%s_move_queue' % board_id)
    board = memval('board_%s' % board_id)
    users = memval('%s_board_users' % board_id)

    is_valid = move_valid(move, board, user_id, users)
    msg = [move, board, user_id, users]
    if is_valid:
        queue.append(move)
        memval('%s_move_queue' % board_id, queue)
        msg = 'ack'
    cxt = {'rsp': msg}
    return HttpResponse(simplejson.dumps(cxt), mimetype="application/json")


@check_login
def data_board(request):
    """ dumps json board data """
    board_id = request.GET['board_id']
    board = memval('board_%s' % board_id)
    board_users = memval('%s_board_users' % board_id)
    val = simplejson.dumps({'board_id': board_id, board_id: board,
                            '%s_board_users': board_users})
    return HttpResponse(val, mimetype="application/json")


def get_account(session):
    if 'account_id' in session:
        try:
            acc = Account.objects.get(pk=session['account_id'])
        except Account.DoesNotExist:
            pass
        else:
            return acc
    return None


@check_login
@render_to("game/select_cell.html")
# TODO: will deleted
def select_cell(request):
    if 'x' in request.GET and 'y' in request.GET:
        x = int(request.GET['x'])
        y = int(request.GET['y'])
        acc = get_account(request.session)
        board_id = request.GET.get('board_id')
        board = memval('board_%s' % board_id)
        users = memval('%s_board_users' % board_id)
        default_bytes = 20
        if with_cells(users, acc):
            return redirect('game.views.play')
        if board[y][x] < default_bytes:
            board[y][x] = default_bytes - board[y][x]
            users[y][x] = [acc.id, '#FF0000']
            memval('board_%s' % board_id, board)
            memval('%s_board_users' % board_id, users)
            return redirect('game.views.play')

    return {'board': memval('board_%s' % board_id)}
