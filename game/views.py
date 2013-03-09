from decorators import render_to, check_login
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.utils import simplejson

from security.models import Account
from utils import memval, move_valid, game_restart as game_start


@check_login
@render_to('game/animation.html')
def board(request):
    ctx = {'user_id': request.session.get('account_id')}
    return ctx


def progress(request):
    """ dumps game progress in json """
    board_id = request.GET['board_id']
    # TODO apply board id
    board = memval('board')
    board_users = memval('board_users')
    simple_moves = memval('simple_moves')
    val = simplejson.dumps({'moves': simple_moves, board_id: board,
                            'board_id': board_id, 'board_users': board_users})
    return HttpResponse(val, mimetype="application/json")


def game_restart(request):
    game_start()
    return HttpResponseRedirect(reverse('homepage'))


def move(request):
    """ adds the move to move list """
    ax = request.GET['fx'];
    ay = request.GET['fy'];
    bx = request.GET['tx'];
    by = request.GET['ty'];
    move = (int(ax), int(ay), int(bx), int(by))
    user_id = int(request.session.get('account_id'));

    # TODO apply board_id
    queue = memval('move_queue')
    board = memval('board')
    users = memval('board_users')

    is_valid = move_valid(move, board, user_id, users)
    msg = [move, board, user_id, users]
    if is_valid:
        queue.append(move)
        memval('move_queue', queue)
        msg = 'ack'
    cxt = {'rsp': msg}
    return HttpResponse(simplejson.dumps(cxt), mimetype="application/json")


def data_board(request):
    """ dumps json board data """
    board_id = request.GET['board_id']
    # TODO validate board_id
    board = memval('board')  # TODO get by board_id
    board_users = memval('board_users')
    val = simplejson.dumps({'board_id': board_id, board_id: board,
                            'board_users': board_users})
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
def select_cell(request):
    if 'x' in request.GET and 'y' in request.GET:
        x = int(request.GET['x'])
        y = int(request.GET['y'])
        acc = get_account(request.session)
        board = memval('board')
        users = memval('board_users')
        default_bytes = 20
        if board[y][x] < default_bytes:
            board[y][x] = default_bytes - board[y][x]
            users[y][x] = [acc.id, acc.id]
            memval('board', board)
            memval('board_users', users)
            return redirect('homepage')

    return {'board': memval('board')}
