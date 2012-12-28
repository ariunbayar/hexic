#!/usr/bin/env python2.7
# coding: utf-8
from contextlib import closing
from main import app, connect_db


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('./schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


init_db()

"""
import main
import db


db.init_db()


from user.models import User


users = [
    {"name": u"Ариунбаяр", "phone": "99437911", "code": "1234",
        "is_admin": True},
]
for user in users:
    db.session.add(User(**user))

db.session.commit()
"""
