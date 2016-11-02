import test_base


class KeysTest(test_base.TestBase):
    def test_200(self):
        result = self._get('/api/v1/keys?code=1')

        self.assertOk(result)
        self.assertJsonContentType(result)
        self.assertJsonEquals(result, {'key': '1'})

    def test_400(self):
        result = self._get('/api/v1/keys')

        self.assertBadRequest(result)
        self.assertJsonContentType(result)
        self.assertJsonEquals(result, {'error': 'missing \'code\' parameter'})

    def _get(self, url):
        return self.app.get(url)
