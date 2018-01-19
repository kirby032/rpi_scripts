'''
This is the sensor baseclass
'''

import logging

logger = logging.getLogger(__name__)

class Sensor(object):
    '''Base class for all sensors'''

    def __init__(self, config, triggerHandler):
        self.id = config['id']
        self.triggerHandler = triggerHandler

    def __str__(self):
        return '{}, Type: {}'.format(self.id, self.__class__.__name__)
