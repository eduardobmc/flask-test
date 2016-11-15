import hashlib
import flask
from flask import current_app as app
from werkzeug import exceptions


blueprint = flask.Blueprint('v1', __name__, url_prefix='/api/v1')


class OutputFile:
    def __init__(self):
        self.size = 0
        self.checksum = hashlib.sha256()

    def write(self, buf):
        self.size += len(buf)
        self.checksum.update(buf)


@blueprint.route('/test')
def index():
    app.logger.info('TEST %d', 1)
    return flask.jsonify(key='value')


@blueprint.route('/error')
def error():
    raise Exception('oh, oh!')


@blueprint.route('/keys')
def keys():
    code = flask.request.args['code']
    return flask.jsonify(key=code)


@blueprint.route('/config')
def config():
    ns = app.config.get_namespace('MYMODULE_')
    return flask.jsonify(ns)


@blueprint.route('/upload', methods=['POST'])
def upload():
    results = []
    storages = flask.request.files.getlist('files')
    for storage in storages:
        output = OutputFile()
        storage.save(output)
        result = {
          'size': output.size,
          'filename': storage.filename,
          'sha256': output.checksum.hexdigest()
        }
        results.append(result)
        app.logger.info(
          'filename="%(filename)s" '
          'size=%(size)d '
          'sha256="%(sha256)s"' % result
        )
    return flask.jsonify(files=results)


@blueprint.route('/crud')
def crud_get():
    return flask.jsonify(method=flask.request.method)


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
