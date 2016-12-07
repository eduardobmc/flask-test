import io
import unittest

from mymodule import utils


class YieldUntilTest(unittest.TestCase):
    def setUp(self):
        content = b'012|456|789|ab'
        stream = io.BytesIO(content)
        self.reader = io.BufferedReader(stream)

    def test_yield_until(self):
        iterator = utils.yield_until(self.reader, b'6|7', size=4)
        self.assertEquals(next(iterator), b'012|')
        self.assertEquals(next(iterator), b'45')
        self.assertRaises(StopIteration, next, iterator)
        self.assertEquals(self.reader.read(), b'6|789|ab')

    def test_yield_size(self):
        iterator = utils.yield_until(self.reader, b'9|a', size=4)
        self.assertEquals(next(iterator), b'012|')
        self.assertEquals(next(iterator), b'456|')
        self.assertEquals(next(iterator), b'78')
        self.assertRaises(StopIteration, next, iterator)
        self.assertEquals(self.reader.read(), b'9|ab')

    def test_yield_upper_half(self):
        iterator = utils.yield_until(self.reader, b'56', size=4)
        self.assertEquals(next(iterator), b'012|')
        self.assertEquals(next(iterator), b'4')
        self.assertRaises(StopIteration, next, iterator)
        self.assertEquals(self.reader.read(), b'56|789|ab')

    def test_yield_not_found(self):
        iterator = utils.yield_until(self.reader, b'xyz', size=4)
        self.assertEquals(next(iterator), b'012|')
        self.assertEquals(next(iterator), b'456|')
        self.assertEquals(next(iterator), b'789|')
        self.assertEquals(next(iterator), b'ab')
        self.assertRaises(StopIteration, next, iterator)

    def test_skip(self):
        iterator = utils.yield_until(self.reader, b'9|', size=4, skip=True)
        self.assertEquals(next(iterator), b'012|')
        self.assertEquals(next(iterator), b'456|')
        self.assertEquals(next(iterator), b'78')
        self.assertRaises(StopIteration, next, iterator)
        self.assertEquals(self.reader.read(), b'ab')


class ReadUntilTest(unittest.TestCase):
    def setUp(self):
        content = b'abcdefgh'
        stream = io.BytesIO(content)
        self.reader = io.BufferedReader(stream)

    def test_read_until(self):
        self.assertEquals(utils.read_until(self.reader, b'efg'), b'abcd')
        self.assertEquals(self.reader.read(), b'efgh')

    def test_read_until_not_found(self):
        self.assertEquals(utils.read_until(self.reader, b'xyz'), b'abcdefgh')
        self.assertEquals(self.reader.read(), b'')

    def test_skip(self):
        data = utils.read_until(self.reader, b'efg', skip=True)
        self.assertEquals(data, b'abcd')
        self.assertEquals(self.reader.read(), b'h')


class ParserTest(unittest.TestCase):
    def test_headers(self):
        data = (
          b'Content-Disposition: form-data; name="files"; filename="test"\r\n'
          b'Content-Type: application/octet-stream\r\n'
          b'\r\n'
          b'some data ...'
        )
        stream = io.BytesIO(data)
        reader = io.BufferedReader(stream)
        headers = utils.read_headers(reader)
        self.assertEquals(headers, {
          'name': 'files',
          'filename': 'test',
          'content-type': 'application/octet-stream'
        })

    def test_parser(self):
        data = (
          b'--boundary\r\n'
          b'Content-Disposition: form-data; name="files"; filename="a"\r\n'
          b'Content-Type: text/plain\r\n'
          b'\r\n'
          b'DATA A\r\n'
          b'--boundary\r\n'
          b'Content-Disposition: form-data; name="files"; filename="b"\r\n'
          b'Content-Type: text/plain\r\n'
          b'\r\n'
          b'DATA B\r\n'
          b'--boundary--\r\n'
        )

        stream = io.BytesIO(data)
        reader = io.BufferedReader(stream)
        parser = utils.parse_multipart(reader, b'--boundary')

        h1, p1 = next(parser)
        self.assertEquals(h1, {
          'name': 'files',
          'filename': 'a',
          'content-type': 'text/plain'
        })
        self.assertEquals(b''.join(p1), b'DATA A')

        h2, p2 = next(parser)
        self.assertEquals(h2, {
          'name': 'files',
          'filename': 'b',
          'content-type': 'text/plain'
        })
        self.assertEquals(b''.join(p2), b'DATA B')

        self.assertRaises(StopIteration, next, parser)
