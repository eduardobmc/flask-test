import re
import six


CRLF = b'\r\n'


def read_until(reader, delim):
    chunks = yield_until(reader, delim)
    return b''.join(chunks)


def read_headers(reader):
    found = read_until_part(reader)
    lines = filter(bool, found.split(CRLF))
    raw_headers = {
      h[0].lower(): h[1]
      for h in (line.decode('ascii').split(': ') for line in lines)
    }
    content_disposition = raw_headers['content-disposition']
    headers = {
      k: v for k, v in directives(content_disposition)
    }
    headers.update({
      k.lower(): v
      for k, v in six.iteritems(raw_headers)
      if k.lower() != 'content-disposition'
    })
    return headers


def directives(value):
    r = re.compile(r';\s*([^=]+)="([^"]+)"')
    for m in r.finditer(value):
        yield m.group(1), m.group(2)


def read_until_part(reader):
    delim = CRLF * 2
    data = read_until(reader, delim)
    # reader.read(len(delim))
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


def yield_until(reader, delim, size=65536):
    chunk = _peek(reader, 2 * size)
    while chunk:
        index = chunk.find(delim)
        if index == -1:
            end = min(len(chunk), size)
            yield chunk[:end]
            reader.read(end)
        else:
            yield chunk[:min(index, size)]
            if size < index:
                yield chunk[size:index]
            reader.read(index)
            break
        chunk = _peek(reader, 2 * size)


def _peek(reader, size):
    buf = reader.peek(size)
    return buf[:min(size, len(buf))]
