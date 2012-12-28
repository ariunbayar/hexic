from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, event
from sqlalchemy.orm import mapper

import db
from helpers import cache_get, cache_set


def after_update_listener(mapper, connection, target):
    if isinstance(target, User):
        cache_set('User%s' % target.id, target)

event.listen(mapper, 'after_update', after_update_listener)


class User(object):
    query = db.session.query_property()

    def __init__(self, **values):
        self.id = values.get('id', None)
        self.name = values.get('name', None)
        self.email = values.get('email', None)
        self.phone = values.get('phone', None)
        self.code = values.get('code', None)
        self.created = values.get('created', None)
        self.last_seen = values.get('last_seen', None)
        self.is_admin = values.get('is_admin', False)

    def __repr__(self):
        columns = sorted(self.__dict__)
        attrs = [repr(getattr(self, k)) for k in columns if k[:4] != '_sa_']
        return '<User %s>' % ' '.join(attrs)

    def cache_update(self):
        cache_set('User%s' % self.id, self)

    @classmethod
    def get_user(cls, id=None):
        def func():
            if id:
                return cls.query.get(id)
            return None
        return cache_get('User%s' % id, func)

    @classmethod
    def get_all(cls):
        def func():
            return [user.id for user in cls.query.all()]
        return [cls.get_user(id) for id in cache_get('user_ids', func)]


users = Table('users', db.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50), unique=True, nullable=False),
    Column('email', String(120)),
    Column('phone', Integer, unique=True, nullable=False),
    Column('code', Integer, nullable=False),
    Column('created', DateTime, default=datetime.now(), nullable=False),
    Column('last_seen', DateTime),
    Column('is_admin', Boolean, default=False),
)

mapper(User, users)
