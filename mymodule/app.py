import flask
from werkzeug import exceptions
from mymodule.blueprints import api_v1


def create_app():
    app = flask.Flask(__name__)
    app.register_blueprint(api_v1.blueprint)
    app.register_error_handler(exceptions.BadRequest, bad_request)
    app.register_error_handler(Exception, exception_handler)
    return app


def bad_request(e):
    return flask.jsonify(error=e.description), e.code


def exception_handler(e):
    flask.current_app.logger.exception(e)
    return flask.jsonify(error=str(e)), 500
