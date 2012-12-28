from datetime import datetime
from flask import render_template, redirect as flask_redirect, url_for
from flask import current_app, g
from wtforms.validators import ValidationError


def template(*args, **kwargs):
    return render_template(*args, **kwargs)


def redirect(uri, *args, **kwargs):
    return flask_redirect(url_for(uri), *args, **kwargs)


def query_db(query, args=(), one=False):
    cursor = g.db.execute(query, args)
    result = [dict((cursor.description[k][0], v)
                   for k, v in enumerate(row)) for row in cursor.fetchall()]
    return (result[0] if result else None) if one else result


def cache_set(key, *args, **kwargs):
    cache_track(key, False)
    return current_app.cache.set(key, *args, **kwargs)


def cache_get(key, func=None, timeout=None):
    value = current_app.cache.get(key)
    cache_track(key)
    if value is None and func is not None:
        timeout = timeout or current_app.config['MEMCACHE_TIMEOUT']
        value = func()
        if not (value is None):
            cache_set(key, value, timeout)
    return value


def cache_track(key, hit=True):
    key_for_keys = current_app.config['MEMCACHE_KEYS']
    keys = current_app.cache.get(key_for_keys) or []
    if key not in keys:
        keys.append(key)
    current_app.cache.set(key_for_keys, keys)
    hit_ratio = current_app.cache.get('hit_ratio_%s' % key) or [0, 0]
    hit_ratio[0 if hit else 1] += 1
    current_app.cache.set('hit_ratio_%s' % key, hit_ratio)


class ValidatorUnique(object):
    def __init__(self, model, field, message=None):
        self.message = message
        self.field = field
        self.model = model

    def __call__(self, form, field):
        if field.data:
            objs = self.model.query.filter(self.field == field.data)
            existing = 0
            if form.uid:
                for obj in objs:
                    existing += 1 if form.uid == obj.id else 0
            if objs.count() - existing > 0:
                d = {"value": field.data}
                if self.message is None:
                    self.message = "Already exists: %(value)s"
                raise ValidationError(self.message % d)


class Property(object):
    _name = None

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.value

    def _set_value(self, instance, value):
        instance._values[self._name] = value


class IntegerProperty(Property):
    def __init__(self, default=None):
        self.value = default

    def __set__(self, instance, value):
        if value is None:
            pass
        elif type(value) is not int:
            raise ValueError('Integer value expected. %s supplied instead'
                             % type(value))
        self.value = value


class TextProperty(Property):
    def __init__(self, default=None):
        self.value = default

    def __set__(self, instance, value):
        if value is not None:
            value = unicode(value)
        self.value = value


class DateTimeProperty(Property):
    def __init__(self, default=None):
        self.value = default

    def __set__(self, instance, value):
        if value is None:
            pass
        elif type(value) is unicode:
            value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        elif type(value) is not datetime:
            raise ValueError('Datetime value expected. %s supplied instead'
                             % type(value))
        self.value = value


class BooleanProperty(Property):
    def __init__(self, default=False):
        self.value = default

    def __set__(self, instance, value):
        if type(value) is int:
            value = bool(int)
        elif type(value) is not bool:
            raise ValueError('Boolean value expected. %s supplied instead'
                             % type(value))
        self.value = value


class Query(object):
    def __init__(self, fields, args, model, query='SELECT'):
        self.fields = fields
        self.args = args
        self.results = None
        self.model = model
        self.index = 0
        self.query_type = query

    def __iter__(self):
        return self

    def select_query(self):
        if self.query_type != 'SELECT':
            raise ValueError('Cannot run %s query. Expected SELECT'
                             % self.query_type)
        sql = 'SELECT * FROM %s' % self.model._table_name
        if self.fields:
            sql += ' WHERE %s' % ','.join('%s==?' % f for f in self.fields)
        return sql

    def get(self):
        return self.next()

    def next(self):
        if self.results is None:
            self.results = query_db(self.select_query(), self.args)
        if len(self.results) > self.index:
            result = self.results[self.index]
            self.index += 1
            return self.model(**result)
        else:
            self.index = 0
            raise StopIteration

class Model(object):
    def __init__(self, **kwargs):
        self.validate(**kwargs)

        #cls = self.__class__
        for field, value in kwargs.iteritems():
            setattr(self, field, value)
            #prop = getattr(cls, field)
            #prop._set_value(self, value)

    def __repr__(self):
        fields = self._get_properties()
        props = ['%s=%r' % (field, getattr(self, field)) for field in fields]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(props))

    def _get_properties(self):
        if not hasattr(self, '_properties'):
            self._properties = []
            for prop in dir(self):
                if isinstance(getattr(self.__class__, prop, None), Property):
                    self._properties.append(prop)
            self._properties.sort()
        return self._properties

    def save(self):
        fields = self._get_properties()
        values = [getattr(self, field) for field in fields]
        return Query(fields, values, self.__class__, 'INSERT')
            

    @classmethod
    def validate(cls, **kwargs):
        for field, value in kwargs.iteritems():
            if not isinstance(getattr(cls, field, None), Property):
                raise ValueError('Invalid property %s' % field)

    @classmethod
    def query(cls, **kwargs):
        cls.validate(**kwargs)
        return Query(kwargs.keys(), kwargs.values(), cls)
