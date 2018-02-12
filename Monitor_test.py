# pylint: disable=missing-docstring
import json
import unittest

import mock

from Monitor import Monitor
from reporting.Reporter import Reporter

class TestMonitor(unittest.TestCase):
    EMPTY_CONFIG = json.loads('{}')

    def test_create_empty_config(self):
        Monitor(self.EMPTY_CONFIG)

    @mock.patch('reporting.Reporter.Reporter.send',
        side_effect=lambda msg, event: event.set())
    def test_sensor_trigger(self, reporter_send):
        reporter = Reporter(json.loads('{ "id": "testReporter" }'))
        monitor = Monitor(self.EMPTY_CONFIG)
        monitor.reporters.append(reporter)

        events = monitor.sensorTrigger('testSensor')

        for event in events:
            event.wait()

        reporter_send.assert_called_once_with(
            'Sensor testSensor was triggered!', events[0])

    @mock.patch('util.reporterFactory.buildReporterFromConfig')
    @mock.patch('util.sensorFactory.buildSensorFromConfig')
    def test_real_init_workflow(self, buildSensor, buildReporter):
        config = '''
        {
            "reporters":[
                "reporter1",
                "reporter2"
            ],
            "sensors":[
                "sensor1",
                "sensor2",
                "sensor3"
            ]
        }
        '''
        monitor = Monitor(json.loads(config))

        self.assertIs(len(monitor.getReporters()), 2)
        buildReporter.assert_has_calls([mock.call('reporter1'),
            mock.call('reporter2')])

        self.assertIs(len(monitor.getSensors()), 3)
        buildSensor.assert_has_calls([
            mock.call('sensor1', monitor.sensorTrigger),
            mock.call('sensor2', monitor.sensorTrigger),
            mock.call('sensor3', monitor.sensorTrigger)])

if __name__ == '__main__':
    unittest.main()
