import json
import unittest
import mymodule


class TestBase(unittest.TestCase):
    def setUp(self):
        mymodule.app.testing = True
        self.app = mymodule.app.test_client()

    def test_404(self):
        result = self.app.get('/api/v1/404')
        self.assertNotFound(result)

    def assertOk(self, result):
        self.assertEquals(result.status_code, 200)

    def assertNotFound(self, result):
        self.assertEquals(result.status_code, 404)

    def assertBadRequest(self, result):
        self.assertEquals(result.status_code, 400)

    def assertInternalServerError(self, result):
        self.assertEquals(result.status_code, 500)

    def assertJsonContentType(self, result):
        self.assertEquals(result.content_type, 'application/json')

    def assertJsonEquals(self, result, expected):
        data = self.getJsonData(result)
        self.assertEquals(data, expected)

    def getJsonData(self, result):
        return json.loads(result.get_data().decode('utf-8'))
