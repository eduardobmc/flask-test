import test_base


class TestTest(test_base.TestBase):
    def test_200(self):
        result = self._get()

        self.assertOk(result)
        self.assertJsonContentType(result)
        self.assertJsonEquals(result, {'key': 'value'})

    def _get(self):
        return self.app.get('/api/v1/test')
