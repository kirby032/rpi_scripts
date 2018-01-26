# pylint: disable=missing-docstring
import json
import unittest

from reporting.SMTPReporter import SMTPReporter

class TestSMTPReporter(unittest.TestCase):
    EMPTY_CONFIG = json.loads('{}')

    def test_init_with_no_config(self):
        with self.assertRaises(KeyError):
            SMTPReporter(self.EMPTY_CONFIG)

if __name__ == '__main__':
    unittest.main()
