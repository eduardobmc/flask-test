import flask
from werkzeug import exceptions
from mymodule import utils


log = utils.get_logger(__name__)
blueprint = flask.Blueprint('v1', __name__, url_prefix='/api/v1')


@blueprint.route('/test')
def index():
    log.info('TEST')
    return flask.jsonify(key='value')


@blueprint.route('/error')
def error():
    raise Exception('oh, oh!')


@blueprint.route('/keys')
def keys():
    code = flask.request.args['code']
    return flask.jsonify(key=code)


@blueprint.route('/crud')
def crud_get():
    return flask.jsonify(method=flask.request.method)


@blueprint.route('/config')
def config():
    app = flask.current_app
    ns = app.config.get_namespace('MYMODULE_')
    return flask.jsonify(ns)


@blueprint.route('/crud', methods=['POST'])
def crud_post():
    payload = flask.request.get_json()
    if payload is None:
        raise exceptions.BadRequest('no post data')
    return flask.jsonify(args=payload)


@blueprint.errorhandler(exceptions.BadRequestKeyError)
def bad_request_key_error(e):
    message = 'missing \'%s\' parameter' % e.args[0]
    return flask.jsonify(error=message), e.code
