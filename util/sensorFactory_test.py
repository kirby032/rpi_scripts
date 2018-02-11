# pylint: disable=missing-docstring
import collections
import random
import unittest

import mock

from util.classes import Object

class TestSensorFactoryPreImport(unittest.TestCase):
    def setUp(self):
        self.patches = []
        self.sensors = []

        # Import the real module
        self.sensorFactory = __import__(
            'util.sensorFactory', globals(), locals(),
            ['buildSensorFromConfig'], -1)

        # Mock import so sensorFactory can try to import fake modules
        self.real_import = __import__
        p = mock.patch('__builtin__.__import__', side_effect=self.fakeImport)
        self.patches.append(p)
        p.start()

    def tearDown(self):
        for patch in self.patches:
            patch.stop()

    # pylint: disable=dangerous-default-value
    def fakeImport(self, pkgName, _globals=globals(),
            _locals=locals(), _fromlist=[], _level=-1):
        '''
        This function will replace the call to import. We generally want this
        to be a pass through unless the import is specifically for our fake
        sensor modules
        '''
        if pkgName in self.sensors:
            val = Object()
            setattr(val, pkgName[len('sensors.'):], Object())
            setattr(getattr(val, pkgName[len('sensors.'):]),
                pkgName[len('sensors.'):], mock.Mock())
            return val

        return self.real_import(pkgName, _globals, _locals, _fromlist, _level)

    def mockIterModulesWithSensors(self, sensors):
        '''
        Mock out pkgutil.iter_modules to return the passed in set of sensors
        '''
        self.assertTrue(isinstance(sensors, collections.Sequence))

        p = mock.patch('pkgutil.iter_modules',
            return_value=[(None, s, False) for s in sensors])
        self.patches.append(p)
        p.start()

    def createSensorsArray(self, numSensors, defaultSensor=True):
        sensors = []
        if defaultSensor:
            sensors.append('Sensor')

        # Of the form 'sensors.My###Sensor'
        self.sensors = ['sensors.My' + str(num) + 'Sensor' \
            for num in range(1, numSensors + 1)]

        # Of the form 'My###Sensor' a 'sensors.' will be prepended by
        # sensorFactory.py when trying to import the modules
        sensors.extend(['My' + str(num) + 'Sensor' \
            for num in range(1, numSensors + 1)])

        return sensors

    def do_test_with_num_sensors(self, numSensors, defaultSensor=True):
        self.mockIterModulesWithSensors(
            self.createSensorsArray(numSensors, defaultSensor))
        reload(self.sensorFactory)
        self.assertEqual(len(self.sensorFactory.sensorClasses), numSensors)

    def test_no_sensors_defined(self):
        with self.assertRaisesRegexp(KeyError,
                'Could not find Sensor.py. Must have a base class in order ' +
                'to define sensors'):
            self.do_test_with_num_sensors(0, False)

    def test_with_only_base_sensor(self):
        self.do_test_with_num_sensors(0)

    def test_with_random_non_base_sensors(self):
        with self.assertRaisesRegexp(KeyError,
                'Could not find Sensor.py. Must have a base class in order ' +
                'to define sensors'):
            self.do_test_with_num_sensors(random.randint(1, 101), False)

    def test_with_one_other_sensor(self):
        self.do_test_with_num_sensors(1)

    def test_with_random_num_sensors(self):
        self.do_test_with_num_sensors(random.randint(2, 101))

class TestSensorFactoryPostImport(unittest.TestCase):
    def setUp(self):
        self.buildSensorFromConfig = __import__('util.sensorFactory',
            globals(), locals(), ['buildSensorFromConfig'], -1) \
            .__getattribute__('buildSensorFromConfig')

    def test_build_generic_sensor(self):
        with self.assertRaises(KeyError):
            self.buildSensorFromConfig(
                {'type': 'Sensor', 'id': 'myBaseSensor'}, lambda: 0)

    def test_build_invalid_sensor(self):
        # XXX: Should make this KeyError more explict exception
        with self.assertRaises(KeyError):
            self.buildSensorFromConfig(
                {'type': 'NonExistent', 'id': 'myFakeSensor'}, lambda: 0)

    def test_build_MagSwitchSensor(self):
        from sensors.MagSwitchSensor import MagSwitchSensor
        sensor = self.buildSensorFromConfig(
            {'type': 'MagSwitchSensor', 'id': 'magSensor1', 'data': {
                "edge_type": "rising",
                "input_pin": 26,
                "delay": 60}}, lambda: 0)

        self.assertEqual(sensor.id, 'magSensor1')
        self.assertTrue(isinstance(sensor, MagSwitchSensor))
