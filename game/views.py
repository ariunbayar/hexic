# coding: utf-8
from decorators import render_to, check_login
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import simplejson
from django.core.urlresolvers import reverse

from game.models import Board
from game.forms import NewBoardForm
from security.models import Account
from django.conf import settings
from utils import (memval, move_valid, game_restart as game_start,
                   random_cell, with_cells)


@check_login
@render_to('game/play.html')
def play(request):
    user_id = request.session.get('account_id')
    account = Account.objects.get(pk=user_id)
    board_id = request.GET.get('board_id', None)

    qs_active_boards = Board.objects.filter(status=Board.STATUS_IN_PROGRESS)
    active_board = qs_active_boards.get(pk=board_id)
    if board_id and active_board:
        board = memval('board_%s' % board_id)

    ctx = {
        'user_id': user_id,
        'update_interval': settings.UPDATE_INTERVAL,
        'active_board': active_board,
    }

    board = memval('board_%s' % board_id)
    users = memval('%s_board_users' % board_id)
    if not with_cells(users, account):
        # Automatically select cell if cell not selected
        default_bytes = 20
        y, x = random_cell(board, users)

        board[y][x] = default_bytes - board[y][x]
        users[y][x] = [account.id, '#FF0000']
        memval('board_%s' % board_id, board)
        memval('%s_board_users' % board_id, users)
    return ctx


@check_login
@render_to("game/dashboard.html")
def dashboard(request):
    # TODO include number of players of one board
    count_player = 2
    user_id = request.session.get('account_id')
    board_players = [user_id]
    for i in xrange(count_player):
        board_players.append(0)
    if request.POST:
        form = NewBoardForm(request.POST)
        if form.is_valid():
            board = Board(
                    name=form.cleaned_data['name'],
                    status=Board.STATUS_WAITING,
                    players=board_players)
            board.save()
            return redirect(reverse('game.views.play') + '?board_id=%s' % board.id)
    else:
        form = NewBoardForm()

    ctx = {
        'active_boards': Board.objects.filter(status=Board.STATUS_IN_PROGRESS),
        'form': form}
    return ctx


@check_login
def select_board(request):
    board_id = request.GET.get('board_id')
    user_id = request.session.get('account_id')
    board = Board.objects.get(board_id)
    indx = board.players.index(0)
    board.players[indx] = user_id
    if indx + 1 == len(board.players):
        board.status = Board.STATUS_IN_PROGRESS
        game_start(board.id)
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
