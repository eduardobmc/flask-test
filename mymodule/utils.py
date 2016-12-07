import six
from six import moves
from werkzeug import http


CRLF = b'\r\n'


def read_until(reader, delim):
    chunks = yield_until(reader, delim)
    return b''.join(chunks)


def read_headers(reader):
    headers = {}
    found = read_until_part(reader)
    for line in moves.filter(bool, found.split(CRLF)):
        name, value = line.decode('ascii').split(': ')
        name = name.lower()
        if name == 'content-disposition':
            headers.update(options(value))
        else:
            headers[name] = value
    return headers


def options(value):
    _, options = http.parse_options_header(value)
    return six.iteritems(options)


def read_until_part(reader):
    delim = CRLF * 2
    data = read_until(reader, delim)
    return data


def parse_multipart(reader, boundary):
    read_until(reader, boundary)
    reader.read(len(boundary))

    while True:
        headers = read_headers(reader)
        reader.read(2 * len(CRLF))

        part = yield_until(reader, CRLF + boundary)
        yield headers, part

        reader.read(len(CRLF + boundary))
        end = reader.peek()
        if len(end) == 0 or end == b'--' + CRLF:
            break


def yield_until(reader, delim, size=65536, skip=False):
    for chunk in iter(lambda: _peek(reader, 2 * size), b''):
        index = chunk.find(delim)
        if index == -1:
            end = min(len(chunk), size)
            yield chunk[:end]
            reader.read(end)
        else:
            yield chunk[:min(index, size)]
            if size < index:
                yield chunk[size:index]
            reader.read(index + len(delim) if skip else index)
            break


def _peek(reader, size):
    buf = reader.peek(size)
    return buf[:min(size, len(buf))]
