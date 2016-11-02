import test_base


class ErrorTest(test_base.TestBase):
    def test_500(self):
        result = self._get()
        data = self.getJsonData(result)

        self.assertInternalServerError(result)
        self.assertJsonContentType(result)
        self.assertEqual(data, {'error': 'oh, oh!'})

    def _get(self):
        return self.app.get('/api/v1/error')
