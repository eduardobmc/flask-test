import test_base


class CrudTest(test_base.TestBase):
    def test_get(self):
        result = self._get()

        self.assertOk(result)
        self.assertJsonContentType(result)
        self.assertJsonEquals(result, {'method': 'GET'})

    def test_post(self):
        result = self._post(
            data='{"data": true}',
            content_type='application/json'
        )

        self.assertOk(result)
        self.assertJsonContentType(result)
        self.assertJsonEquals(result, {'args': {'data': True}})

    def test_post_bad_content_type(self):
        result = self._post(
            data='{"data": true}',
            content_type='text/plain'
        )

        self.assertBadRequest(result)
        self.assertJsonContentType(result)
        self.assertJsonEquals(result, {'error': 'no post data'})

    def _get(self):
        return self.app.get('/api/v1/crud')

    def _post(self, **kwargs):
        return self.app.post('/api/v1/crud', **kwargs)
