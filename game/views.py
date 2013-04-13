# coding: utf-8
from decorators import render_to, check_login
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import simplejson
from django.core.urlresolvers import reverse

from game.models import HexicProfile, Board
from game.forms import NewBoardForm
from security.models import Account
from django.conf import settings
from utils import (memval, move_valid, game_restart as game_start,
                   random_cell, with_cells)


def get_hexic_profile_by_acc(account):
    obj, created = HexicProfile.objects.get_or_create(account=account)
    return obj

@check_login
@render_to('game/animation.html')
def board(request):
    user_id = request.session.get('account_id')
    account = Account.objects.get(pk=user_id)
    profile = get_hexic_profile_by_acc(account)
    if request.GET.get('color'):
        profile.color = '#' + request.GET.get('color')
        profile.save()
    board_id = request.GET.get('board_id', None)

    qs_active_boards = Board.objects.filter(status=Board.STATUS_IN_PROGRESS)
    if board_id and qs_active_boards.get(pk=board_id):
        board = memval('board_%s' % board_id)

    ctx = {
        'profile': profile,
        'user_id': user_id,
        'colors': ['90CA77', '81C6DD', 'E9B64D', 'E48743', '9E3B33'],
        'update_interval': settings.UPDATE_INTERVAL,
        'board_id': board_id,
    }

    board = memval('board_%s' % board_id)
    users = memval('%s_board_users' % board_id)
    if not with_cells(users, account):
        # Automatically select cell if cell not selected
        default_bytes = 20
        y, x = random_cell(board, users)

        board[y][x] = default_bytes - board[y][x]
        profile = HexicProfile.objects.get(account=account)
        users[y][x] = [account.id, profile.color]
        memval('board_%s' % board_id, board)
        memval('%s_board_users' % board_id, users)
    return ctx


@check_login
@render_to("game/select_board.html")
def select_board(request):
    if request.POST:
        form = NewBoardForm(request.POST)
        if form.is_valid():
            board_name = form.cleaned_data['name']
            qs = Board.objects.filter(
                    name=board_name,
                    status=Board.STATUS_IN_PROGRESS)
            name_exist = (qs.count() > 0)
            if not name_exist:
                board = Board(
                        name=board_name,
                        status=Board.STATUS_IN_PROGRESS)
                board.save()
                board_id = board.id
                game_start(board_id)
                return redirect(reverse('homepage') + '?board_id=%s' % board_id)
            msg = 'Нэр давхцсан байна'
            form._errors['name'] = form.error_class([msg])
    else:
        form = NewBoardForm()

    ctx = {
        'active_boards': Board.objects.filter(status=Board.STATUS_IN_PROGRESS),
        'form': form}
    return ctx


def progress(request):
    """ dumps game progress in json """
    board_id = request.GET.get('board_id')
    board = memval('board_%s' % board_id)
    board_users = memval('%s_board_users' % board_id)
    simple_moves = memval('%s_simple_moves' % board_id)
    val = simplejson.dumps({'moves': simple_moves, board_id: board,
                            'board_id': board_id, 'board_users': board_users})
    return HttpResponse(val, mimetype="application/json")


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
            return redirect('homepage')
        if board[y][x] < default_bytes:
            board[y][x] = default_bytes - board[y][x]
            profile = HexicProfile.objects.get(account=acc)
            users[y][x] = [acc.id, profile.color]
            memval('board_%s' % board_id, board)
            memval('%s_board_users' % board_id, users)
            return redirect('homepage')

    return {'board': memval('board_%s' % board_id)}
