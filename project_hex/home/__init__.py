import flask

home = flask.Blueprint('home', __name__, template_folder="templates")

from . import views
