import os
import hashlib
import pytest
from . import test_base


class FakeFile:
    def __init__(self, size):
        self.size = size
        self.remaining = size
        self.checksum = hashlib.sha256()

    def read(self, n):
        size = min(self.remaining, n)
        self.remaining -= size
        buf = os.urandom(size)
        self.checksum.update(buf)
        return buf


class UploadTest(test_base.TestBase):
    def test_post(self):
        files = [(FakeFile(1 << 20), 'test.file')]
        self._test(files)

    @pytest.mark.slow
    def test_large_post(self):
        files = [(FakeFile(1 << 31), 'test.file')]
        self._test(files)

    def test_multiple_post(self):
        files = [(FakeFile(1 << 20), 'test.%d' % i) for i in range(10)]
        self._test(files)

    def _test(self, files):
        result = self.app.post('/api/v1/upload', data={'files': files})

        self.assertOk(result)
        self.assertJsonContentType(result)
        self.assertJsonEquals(result, {
          'files': [{
            'size': f.size,
            'filename': name,
            'sha256': f.checksum.hexdigest()
          } for f, name in files]
        })
