'''
XXX: docstring
'''
import logging
import pkgutil
from sensors.Sensor import Sensor

logger = logging.getLogger(__name__)

sensorClasses = {}

for _, name, ispkg in pkgutil.iter_modules(['sensors']):
    if not ispkg and name != 'Sensor':
        tempClass = __import__('sensors', globals(), locals(), [name], -1) \
            .__getattribute__(name).__getattribute__(name)
        sensorClasses[name] = tempClass

def buildSensorFromConfig(config, triggerHandler):
    '''
    Reads the config for the type of sensor and instantiates that type

    Args:
        config: The configuration dict for this sensor
        triggerHandler: The callback handler when the sensor triggers

    Returns:
        sensor: The sensor of the appropriate class as indicated by the config
    '''
    return sensorClasses[config['type']](config, triggerHandler)
