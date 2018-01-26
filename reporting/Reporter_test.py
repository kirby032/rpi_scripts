# pylint: disable=missing-docstring
import json
import unittest

from reporting.Reporter import Reporter

class TestReporter(unittest.TestCase):
    EMPTY_CONFIG = json.loads('{}')

    def test_init_with_no_config(self):
        with self.assertRaises(KeyError):
            Reporter(self.EMPTY_CONFIG)

    def test_init_with_id(self):
        config = '''
        {
            "id": "reporter1"
        }
        '''
        reporter = Reporter(json.loads(config))
        self.assertEqual(reporter.id, "reporter1")

if __name__ == '__main__':
    unittest.main()

