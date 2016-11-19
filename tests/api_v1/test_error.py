from . import test_base


class ErrorTest(test_base.TestBase):
    def test_500(self):
        result = self._get()

        self.assertInternalServerError(result)
        self.assertJsonContentType(result)
        self.assertJsonEquals(result, {'error': 'oh, oh!'})

    def _get(self):
        return self.app.get('/api/v1/error')
