from django.core.cache import cache


def memval(name, value='__empty__', duration=30, allow_empty=False):
    """ get/set memcache value """
    if value == '__empty__': # get case
        value = cache.get(name, None)
        if allow_empty == False and value is None:
            raise Exception('%s is empty while game is active' % name)
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
    is_valid = is_valid and (users[y][x] == user_id)
    return is_valid

def move_fix(move, moves):
    return moves
