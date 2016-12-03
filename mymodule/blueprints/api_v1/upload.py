import io
import re
import hashlib
import flask
from flask import current_app as app

from ... import utils


class OutputFile:
    def __init__(self):
        self.size = 0
        self.checksum = hashlib.sha256()

    def write(self, buf):
        self.size += len(buf)
        self.checksum.update(buf)

    def write_iterable(self, iterable):
        for chunk in iterable:
            self.write(chunk)


def post():
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


def post2():
    wsgi_input = flask.request.environ['wsgi.input']
    stream = get_io_stream(wsgi_input)
    reader = io.BufferedReader(stream, buffer_size=65536)

    boundary = get_boundary(flask.request.content_type)
    parser = utils.parse_multipart(reader, boundary)

    results = []
    for headers, part in parser:
        output = OutputFile()
        output.write_iterable(part)
        result = {
          'size': output.size,
          'filename': headers['filename'],
          'sha256': output.checksum.hexdigest()
        }
        results.append(result)
        app.logger.info(
          'filename="%(filename)s" '
          'size=%(size)d '
          'sha256="%(sha256)s"' % result
        )

    return flask.jsonify(files=results)


def get_io_stream(stream):
    if not isinstance(stream, io.IOBase):  # pragma: no cover
        # Only for python 2.7, where "file" is not io.IOBase
        fd = stream.fileno()
        return io.FileIO(fd, closefd=False)
    return stream


def get_boundary(content_type):
    r = re.compile('boundary="?(?P<boundary>[^"]*)"?')
    m = r.search(content_type)
    boundary = '--' + m.group('boundary')
    return bytearray(boundary, 'ascii')
