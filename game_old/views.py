from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils import simplejson
from decorators import check_login, render_to

from game.models import HexicProfile
from security.models import Account
from game.utils import memval, move_valid, game_restart as game_start


def game_stop():
    cache.delete('board')
    cache.delete('moves')
    cache.delete('move_queue')
    cache.delete('simple_moves')


@check_login
def home(request):
    """adjacencies:
    |  board  | matrix | expression
    |  1 2 a  | 1 2 a  | [x-1][y-1]  [x][y-1]
    | 3 0 4   | 3 0 4  | [x-1][y]    [x][y]
    |  5 6 c  | 5 6 c  | [x-1][y+1]  [x][y+1]
    """
    board_id = 'board1'
    cxt = {'user_id': request.session.get('account_id'), 'board_id': board_id}
    return render_to_response('game/home.html', RequestContext(request, cxt))


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
            profile = HexicProfile.objects.get(account=acc)
            users[y][x] = [acc.id, profile.color]
            memval('board', board)
            memval('board_users', users)
            return redirect('homepage')

    return {'board': memval('board')}
