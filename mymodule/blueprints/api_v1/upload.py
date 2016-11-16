import hashlib
import flask


class OutputFile:
    def __init__(self):
        self.size = 0
        self.checksum = hashlib.sha256()

    def write(self, buf):
        self.size += len(buf)
        self.checksum.update(buf)


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
        flask.current_app.logger.info(
          'filename="%(filename)s" '
          'size=%(size)d '
          'sha256="%(sha256)s"' % result
        )
    return flask.jsonify(files=results)
