'''
XXX: docstring
'''
import logging
import pkgutil

logger = logging.getLogger(__name__)

sensorClasses = {}

foundBaseClass = False
for _, name, ispkg in pkgutil.iter_modules(['sensors']):
    if name == 'Sensor':
        foundBaseClass = True
    if not ispkg and name != 'Sensor' and name[-5:] != '_test':
        tempClass = __import__('sensors.' + name, globals(), locals(), [], -1) \
            .__getattribute__(name).__getattribute__(name)
        sensorClasses[name] = tempClass
if not foundBaseClass:
    raise KeyError('Could not find Sensor.py. Must have a base class in ' +
        'order to define sensors')

logger.info('Found %d sensor classes', len(sensorClasses))
if logger.isEnabledFor(logging.DEBUG):
    logger.debug('Sensor Classes:')
    for sensorClass in sensorClasses:
        logger.debug('\t%s', sensorClasses[sensorClass].__name__)

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
