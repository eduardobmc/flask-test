import flask
from werkzeug import exceptions
from .blueprints import api_v1


app = flask.Flask(__name__)
app.register_blueprint(api_v1.blueprint)


@app.errorhandler(exceptions.BadRequest)
def bad_request(e):
    return flask.jsonify(error=e.description), e.code


@app.errorhandler(Exception)
def exception_handler(e):
    app.logger.exception(e)
    return flask.jsonify(error=str(e)), 500
