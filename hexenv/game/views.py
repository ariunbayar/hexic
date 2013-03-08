from collections import deque
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils import simplejson
from player.decorators import login_required
from player.helpers import get_player

from game.utils import memval, move_valid

def get_new_board():
    board = []
    for y in range(10):
        board.append([10 for x in range(10)])
    return board

def get_new_board_users():
    board_users = []
    for y in range(10):
        board_users.append([[0, 0] for x in range(10)])
    return board_users;

def game_start():
    board = get_new_board()
    board_users = get_new_board_users()
    moves = {}
    queue = deque([])
    simple_moves = []
    cache.set('board', board, 60)
    cache.set('board_users', board_users, 60)
    cache.set('moves', moves, 60)
    cache.set('move_queue', queue, 60)
    cache.set('simple_moves', simple_moves, 60)

def game_stop():
    cache.delete('board')
    cache.delete('moves')
    cache.delete('move_queue')
    cache.delete('simple_moves')

@login_required
def home(request):
    """adjacencies:
    |  board  | matrix | expression
    |  1 2 a  | 1 2 a  | [x-1][y-1]  [x][y-1]
    | 3 0 4   | 3 0 4  | [x-1][y]    [x][y]
    |  5 6 c  | 5 6 c  | [x-1][y+1]  [x][y+1]
    """
    board_id = 'board1'
    cxt = {'user_id': request.session.get('id'), 'board_id': board_id}
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
    board_id = request.GET['board_id'];
    user_id = int(request.GET['user_id']);  # TODO change this to session

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

@login_required
def select_cell(request):
    if 'x' in request.GET and 'y' in request.GET:
        x = int(request.GET['x'])
        y = int(request.GET['y'])
        player = get_player(request.session)
        board = memval('board')
        users = memval('board_users')
        if board[y][x] < player.bytes:
            board[y][x] = player.bytes - board[y][x]
            users[y][x] = [player.id, player.design]
            memval('board', board)
            memval('board_users', users)
            return HttpResponseRedirect(reverse('homepage'))

    cxt = {'board': memval('board')}
    return render_to_response('game/select_cell.html', cxt)
