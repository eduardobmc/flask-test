import mymodule
import test_base


class ConfigTest(test_base.TestBase):
    def setUp(self):
        super(ConfigTest, self).setUp()
        mymodule.app.config['MYMODULE_TEST'] = 'testing'

    def test_get(self):
        result = self._get()

        self.assertOk(result)
        self.assertJsonContentType(result)
        self.assertJsonEquals(result, {'test': 'testing'})

    def _get(self):
        return self.app.get('/api/v1/config')
