# pylint: disable=missing-docstring
# pylint: disable=no-self-use
import json
import unittest
import util.config

class TestValidateConfig(unittest.TestCase):
    def test_no_config(self):
        with self.assertRaises(util.config.ConfigKeyMissingError):
            self.assertTrue(util.config.validateConfig(None, ['1', '2', '3']))

    def test_keys_is_none(self):
        util.config.validateConfig({'data': None}, None)

    def test_keys_is_empty(self):
        util.config.validateConfig({'data': None}, {})

    def test_all_keys_in_config(self):
        config = '''
        {
            "aNumber": 100,
            "anObject": {
                "keyx": "I am an object",
                "id": 27
            },
            "aString": "This is a string",
            "anArray": [1, 2, 3, 4]
        }
        '''

        keys = {
            "key1": "aNumber",
            "key2": "anObject",
            "key3": "aString",
            "key4": "anArray"
        }

        self.assertTrue(util.config.validateConfig(json.loads(config), keys))

if __name__ == '__main__':
    unittest.main()
