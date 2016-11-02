import test_base


class KeysTest(test_base.TestBase):
    def test_200(self):
        result = self._get('/api/v1/keys?code=1')
        data = self.getJsonData(result)

        self.assertOk(result)
        self.assertJsonContentType(result)
        self.assertEqual(data, {'key': '1'})

    def test_400(self):
        result = self._get('/api/v1/keys')
        data = self.getJsonData(result)

        self.assertBadRequest(result)
        self.assertJsonContentType(result)
        self.assertEqual(data, {'error': 'missing \'code\' parameter'})

    def _get(self, url):
        return self.app.get(url)
