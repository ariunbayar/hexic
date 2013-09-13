import time
# http://docs.python.org/library/collections.html to optimize

from game.models import Board
from game.utils import memval

from django.conf import settings
from datetime import datetime
from django.db import transaction

CELL_LIMIT = 50
MOVE_LIMIT = 489
DEC_GRAPH = [
    0, 0, 1, 2, 3, 3, 4, 4, 5, 5, #  0 -  9
    5, 5, 5, 6, 6, 6, 6, 6, 6, 6, # 10 - 19
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, # 20 - 29
]
DEC_MIN = 29
DEC_DIV = 10
DEC_ADD = 4.3

def get_decrement(number):
    """ Main algorithm for decrementing a cell when moving """
    if DEC_MIN < number:
        n = int(round((number / DEC_DIV) + DEC_ADD))
    else:
        n = DEC_GRAPH[number]
    return n

def process_queue(queue, moves, users):
    """ process queue to moves """
    while len(queue):
        ax, ay, bx, by = queue.popleft()
        aa = "".join([`ax`, "_", `ay`])
        bb = "".join([`bx`, "_", `by`])
        same_user = users[ay][ax] == users[by][bx]
        if (ax, ay) == (bx, by) and same_user:
            moves[aa] = [[ax, ay], [], {}]  # a removal move
        else: # add to the moves
            # [ aa's coordinate, bb and its coordinate, fighters on aa]
            moves[aa] = [[ax, ay], [bb, bx, by], {}]
            if bb not in moves:
                moves[bb] = [[bx, by], [], {}]
            elif len(moves[bb][1]) and moves[bb][1][0] == aa and same_user:
                # (aa -> bb) and (bb -> aa) is unacceptable 
                moves[bb] = [[bx, by], [], {}]
    return moves

def process_board(board_id, board_users):
    board = memval('board_%s' % board_id)
    users = memval(board_users)
    for y, row in enumerate(board):
        for x, v in enumerate(row):
            if board[y][x] > 0 and board[y][x] < CELL_LIMIT \
               and users[y][x][0] > 0:
                board[y][x] += 1
    memval('board_%s' % board_id, board)

def process_moves(moves_name=None, board_id=None, move_queue=None,
        simple_moves=None, board_users=None):
    moves = memval(moves_name, allow_empty=True)
    queue = memval(move_queue)
    board = memval('board_%s' % board_id)
    users = memval(board_users)
    s_moves = []  # simple moves to display on board

    moves = process_queue(queue, moves, users)

    # decrement cells and collect fighters
    for k in moves:
        if len(moves[k][1]) == 0:
            continue
        bb, bx, by = moves[k][1]
        ax, ay = moves[k][0]
        fromuid = users[ay][ax][0]

        n = get_decrement(board[ay][ax]);
        will_overflow = (board[by][bx] + n > MOVE_LIMIT)
        if will_overflow and fromuid == users[by][bx][0]:
            n = MOVE_LIMIT - board[by][bx]
        board[ay][ax] -= n
        if fromuid == users[by][bx][0]:
            board[by][bx] += n  # apply if same user
        else:
            # making non duplicate user ids in fighters
            if fromuid not in moves[bb][2]:
                moves[bb][2][fromuid] = n
            else:
                moves[bb][2][fromuid] += n
        s_moves.append((ax, ay, bx, by))

    # fight and apply the winner
    for k in moves:
        x, y = moves[k][0]
        orig = board[y][x]
        winner_id = 0
        winner_score = 0
        decrementer = 0
        for user_id in moves[k][2]:
            n = moves[k][2][user_id]
            if n > orig:
                if n > winner_score:
                    winner_id = user_id
                    winner_score = n
            else:
                if n > decrementer:
                    decrementer = n
        if winner_id:
            moves[k][1] = []  # remove the move
            users[y][x] = [winner_id, '#FF0000']
            board[y][x] = winner_score - orig
        else:
            board[y][x] -= decrementer
        moves[k][2] = {}

    memval('board_%s' % board_id, board)
    memval(moves_name, moves)
    memval(move_queue, queue)
    memval(simple_moves, s_moves)
    memval(board_users, users)


@transaction.commit_manually
def clear_query_cache():
    transaction.commit()

def main():
    clear_query_cache()
    active_boards = Board.objects.filter(
                    created_at__lte=datetime.now(),
                    status=Board.STATUS_IN_PROGRESS)
    for board in active_boards:
        if not memval('board_%s' % board.id):
            board.status = Board.STATUS_ERROR
            board.save()
            continue
        kwargs = {'moves_name': '%s_moves' % board.id,
                  'move_queue': '%s_move_queue' % board.id,
                  'simple_moves': '%s_simple_moves' % board.id,
                  'board_users': '%s_board_users' % board.id,
                  'board_id': board.id}
        for i in xrange(3):
            process_moves(**kwargs)
            time.sleep(settings.UPDATE_INTERVAL / 1000)
        process_board(kwargs['board_id'], kwargs['board_users'])
