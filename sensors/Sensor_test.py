# pylint: disable=missing-docstring
import json
import unittest

from sensors.Sensor import Sensor

class TestSensor(unittest.TestCase):
    EMPTY_CONFIG = json.loads('{}')

    def test_init_with_no_config(self):
        with self.assertRaises(KeyError):
            Sensor(self.EMPTY_CONFIG, 'myCallback')

    def test_init_with_id(self):
        config = '''
        {
            "id": "testSensor"
        }
        '''
        sensor = Sensor(json.loads(config), 'myCallback')
        self.assertEqual(sensor.id, 'testSensor')

if __name__ == '__main__':
    unittest.main()
