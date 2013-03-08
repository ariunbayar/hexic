from collections import deque
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
        board_users.append([[0, 0] for x in range(10)])
    return board_users;


def game_restart():
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


def memval(name, value='__empty__', duration=30, allow_empty=False):
    """ get/set memcache value """
    if value == '__empty__': # get case
        value = cache.get(name, None)
        if allow_empty == False and value is None:
            msg = '%s is empty while game is active. Restarting...'
            logging.error(msg % name)
            game_restart()
            value = cache.get(name, None)

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
