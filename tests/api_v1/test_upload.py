import hashlib
from . import test_base


class FakeFile:
    def __init__(self, size):
        self.size = size
        self.remaining = size
        self.checksum = hashlib.sha256()

    def read(self, n):
        size = min(self.remaining, n)
        self.remaining -= size
        buf = b'x' * size
        self.checksum.update(buf)
        return buf


class UploadTest(test_base.TestBase):
    LARGE = 2 << 30   # 2 GB
    MEDIUM = 1 << 20  # 1 MB
    SMALL = 1 << 10   # 1 KB

    def test_post(self):
        files = [(FakeFile(self.MEDIUM), 'test.file')]
        self._test('/api/v1/upload', files)

    def test_multiple_post(self):
        files = [(FakeFile(self.MEDIUM), 'test.%d' % i) for i in range(10)]
        self._test('/api/v1/upload', files)

    def test_post2(self):
        files = [(FakeFile(self.LARGE), 'test.file')]
        self._test('/api/v1/upload2', files)

    def test_small_post2(self):
        files = [(FakeFile(self.SMALL), 'test.file')]
        self._test('/api/v1/upload2', files)

    def _test(self, url, files):
        result = self.app.post(url, data={'files': files})

        self.assertOk(result)
        self.assertJsonContentType(result)
        self.assertJsonEquals(result, {
          'files': [{
            'size': f.size,
            'filename': name,
            'sha256': f.checksum.hexdigest()
          } for f, name in files]
        })
