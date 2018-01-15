'''
This is the sensor baseclass
'''

import logging

logger = logging.getLogger(__name__)

class Sensor(object):
    '''Base class for all sensors'''

    def __init__(self, configEntry, triggerHandler):
        self.configEntry = configEntry
        self.triggerHandler = triggerHandler

        logger.debug('Initialized Sensor')
