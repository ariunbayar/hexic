#!/usr/bin/env python2.7
import os
import sys

vendor_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           'vendor')
if vendor_path not in sys.path:
    sys.path[0:0] = [vendor_path]


from flask import Flask, g
import sqlite3
from werkzeug import run_simple
from home import home
from user import user
from admin import admin


app = Flask(__name__)
app.config.from_object('settings')
app.register_blueprint(home)
app.register_blueprint(user)
app.register_blueprint(admin, url_prefix="/admin")
app.secret_key = \
    '\x95\xb3m\xf1h\t\x7f\xad\xd9\xf4I|\xa8\xeaMk\x9c#\x99\xec/\x06\xbd\xe7'


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception=None):
    # Please keep in mind that the teardown request functions are always
    # executed, even if a before-request handler failed or was never executed.
    # Because of this we have to make sure here that the database is there
    # before we close it.
    if hasattr(g, 'db'):
        g.db.close()


# Setup memcached
from werkzeug.contrib.cache import MemcachedCache
app.cache = MemcachedCache(app.config['MEMCACHE'],
                           app.config['MEMCACHE_TIMEOUT'])


if __name__ == "__main__":
    if app.config['PROFILER']:
        from werkzeug.contrib.profiler import ProfilerMiddleware
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app)

    if app.config['DEBUG']:
        kwargs = {'use_reloader': True, 'use_debugger': True}
    else:
        kwargs = {}
    run_simple('0.0.0.0', 5000, app, **kwargs)
