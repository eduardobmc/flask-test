import flask
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import BadRequestKeyError
from .blueprints import api_v1


def create_app():
    app = flask.Flask(__name__)
    app.register_blueprint(api_v1.blueprint)
    app.register_error_handler(BadRequest, _bad_request)
    app.register_error_handler(BadRequestKeyError, _missing_parameter)
    app.register_error_handler(Exception, _exception_handler)
    return app


def _missing_parameter(e):
    message = 'missing \'%s\' parameter' % e.args[0]
    return flask.jsonify(error=message), e.code


def _bad_request(e):
    return flask.jsonify(error=e.description), e.code


def _exception_handler(e):
    flask.current_app.logger.exception(e)
    return flask.jsonify(error=str(e)), 500
