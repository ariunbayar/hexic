from collections import deque
import random
import logging

from django.core.cache import cache


def get_new_board():
    board = []
    for y in range(10):
        board.append([10 for x in range(10)])
    return board


def get_new_board_users():
    board_users = []
    for y in range(10):
        board_users.append([[0, '#aaaaaa'] for x in range(10)])
    return board_users;


def game_start(board_id):
    board = get_new_board()
    board_users = get_new_board_users()
    moves = {}
    queue = deque([])
    simple_moves = []
    cache.set('board_%s' % board_id, board, 60)
    cache.set('%s_board_users' % board_id, board_users, 60)
    cache.set('%s_moves' % board_id, moves, 60)
    cache.set('%s_move_queue' % board_id, queue, 60)
    cache.set('%s_simple_moves' % board_id, simple_moves, 60)


def memval(name, value='__empty__', duration=6*3600, allow_empty=False):
    """ get/set memcache value """
    if value == '__empty__': # get case
        value = cache.get(name, None)
        if allow_empty == False and value is None:
            msg = '%s is empty while game is active.'
            logging.error(msg % name)

        return value
    else:
        cache.set(name, value, duration)

def move_valid(move, board, user_id, users):
    (x, y, x1, y1) = move
    xx = x + (0 if y % 2 else 1)

    is_valid = ((x1 - 1 == x) and (y1 == y))\
               or ((x1 == xx) and (y1 - 1 == y))\
               or ((x1 + 1 == xx) and (y1 - 1 == y))\
               or ((x1 + 1 == x) and (y1 == y))\
               or ((x1 + 1 == xx) and (y1 + 1 == y))\
               or ((x1 == xx) and (y1 + 1 == y))\
               or (x == x1 and y == y1) # not move, a removal
    is_valid = is_valid and (users[y][x][0] == user_id)
    return is_valid

def move_fix(move, moves):
    return moves

def random_cell(board, users):
    """ Returns board's y, x if cell not selected """
    default_bytes = 20
    while True:
        y = random.randint(0, len(board) - 1)
        x = random.randint(0, len(board[y]) - 1)
        if board[y][x] and board[y][x] < default_bytes and not users[y][x][0]:
            return (y, x)

def with_cells(users, acc):
    for _y in xrange(10):
        for _x in xrange(10):
            if acc.id == users[_y][_x][0]:
                return True
    return False
