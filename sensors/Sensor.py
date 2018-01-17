'''
This is the sensor baseclass
'''

import logging

logger = logging.getLogger(__name__)

class Sensor(object):
    '''Base class for all sensors'''

    def __init__(self, config, triggerHandler):
        self.config = config
        self.triggerHandler = triggerHandler

    def __str__(self):
        return 'Sensor \'{}\'\n{}'.format(self.config['id'], self.config)
