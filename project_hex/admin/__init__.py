import flask

admin = flask.Blueprint('admin', __name__, template_folder="templates")

from . import views
