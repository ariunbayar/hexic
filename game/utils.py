import logging
import pickle
import redis


def memval(name, value='__empty__', duration=6*3600, allow_empty=False):
    """ get/set memcache value """
    redis_cache = redis.StrictRedis()  # TODO use settings
    if value == '__empty__': # get case
        value = redis_cache.get(name)
        if allow_empty == False and value is None:
            msg = '%s is empty while game is active.'
            logging.error(msg % name)
        if type(value) is str:
            value = pickle.loads(value)

        return value
    else:
        redis_cache.set(name, pickle.dumps(value), duration)
