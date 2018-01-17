'''
XXX: docstring
'''
import logging

from sensors.Sensor import Sensor

logger = logging.getLogger(__name__)

class MagSwitchSensor(Sensor):
    '''
    XXX: docstring
    '''
    def __init__(self, config, triggerHandler):
        super(MagSwitchSensor, self).__init__(config, triggerHandler)
        logger.debug('Created MagSwitchSensor')
