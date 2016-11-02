import flask
from werkzeug import exceptions, local
from mymodule.blueprints import api_v1


log = local.LocalProxy(lambda: flask.current_app.logger)
app = flask.Flask(__name__)
app.register_blueprint(api_v1.blueprint)


@app.errorhandler(exceptions.NotFound)
def not_found(e):
    return flask.jsonify(error=e.description), e.code


@app.errorhandler(exceptions.BadRequest)
def bad_request(e):
    return flask.jsonify(error=e.description), e.code


@app.errorhandler(Exception)
def exception_handler(e):
    log.exception(e)
    return flask.jsonify(error=str(e)), 500
