from helpers import template
from . import home


@home.route("/")
def index():
    cxt = {'user': 'ari'}
    return template("home/homepage.html", **cxt)


@home.route("/design/")
def design():
    return template("home/design.html")
