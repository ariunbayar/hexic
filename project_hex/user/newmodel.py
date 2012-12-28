from helpers import (IntegerProperty, TextProperty, DateTimeProperty,
                     BooleanProperty)
from helpers import Model


class User(Model):
    _table_name = 'users'

    id = IntegerProperty()
    name = TextProperty()
    email = TextProperty()
    phone = TextProperty()
    code = TextProperty()
    created = DateTimeProperty()
    last_seen = DateTimeProperty()
    is_admin = BooleanProperty()
