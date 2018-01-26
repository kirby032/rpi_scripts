# pylint: disable=missing-docstring
import json
import unittest

from sensors.Sensor import Sensor

class TestSensor(unittest.TestCase):
    EMPTY_CONFIG = json.loads('{}')

    def test_init_with_no_config(self):
        with self.assertRaises(KeyError):
            Sensor(self.EMPTY_CONFIG, 'myCallback')

if __name__ == '__main__':
    unittest.main()
