import flask
from werkzeug import local


def get_app_logger():
    return local.LocalProxy(lambda: flask.current_app.logger)


def get_logger(name):
    return local.LocalProxy(lambda: flask.current_app.logger.getChild(name))
