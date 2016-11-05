import flask
from werkzeug import exceptions
from mymodule import utils
from mymodule.blueprints import api_v1


log = utils.get_app_logger()
app = flask.Flask(__name__)
app.register_blueprint(api_v1.blueprint)


@app.errorhandler(exceptions.BadRequest)
def bad_request(e):
    return flask.jsonify(error=e.description), e.code


@app.errorhandler(Exception)
def exception_handler(e):
    log.exception(e)
    return flask.jsonify(error=str(e)), 500
