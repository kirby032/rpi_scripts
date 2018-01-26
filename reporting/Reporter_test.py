# pylint: disable=missing-docstring
import json
import unittest

from reporting.Reporter import Reporter

class TestReporter(unittest.TestCase):
    EMPTY_CONFIG = json.loads('{}')

    def test_init_with_no_config(self):
        with self.assertRaises(KeyError):
            Reporter(self.EMPTY_CONFIG)

if __name__ == '__main__':
    unittest.main()

