import test_base


class TestTest(test_base.TestBase):
    def test_200(self):
        result = self._get()
        data = self.getJsonData(result)

        self.assertOk(result)
        self.assertJsonContentType(result)
        self.assertEqual(data, {'key': 'value'})

    def _get(self):
        return self.app.get('/api/v1/test')
