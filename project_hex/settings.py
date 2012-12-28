from datetime import timedelta


DEBUG = True
PROFILER = False
DATABASE = './.hex1.db'

MEMCACHE = ['localhost:11211']
MEMCACHE_TIMEOUT = 60 * 60
# memcache key to track all keys saved
MEMCACHE_KEYS = 'hex'

LAST_SEEN_INTERVAL = timedelta(0, 60)  # seconds
