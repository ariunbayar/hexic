import flask

user = flask.Blueprint('user', __name__, template_folder="templates")

from . import views
