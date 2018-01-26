# pylint: disable=missing-docstring
import json
import unittest

from Monitor import Monitor

class TestMonitor(unittest.TestCase):
    def test_create_monitor_empty_config(self):
        monitor = Monitor(json.dumps({}))

if __name__ == '__main__':
    unittest.main()
