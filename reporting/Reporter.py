'''
XXX: docstring
'''

import logging

logger = logging.getLogger(__name__)

class Reporter(object):
    '''
    XXX: docstring
    '''

    def __init__(self, config):
        self.config = config
        self.id = config['id']

    def __str__(self):
        return '{}, Type: {}'.format(self.id, self.__class__.__name__)

    def send(self, msg):
        '''
        XXX: docstring
        '''
        logger.info('Reporting class %s has no send handler',
            self.__class__.__name__)
        logger.info('Failed to report message: \'%s\'', msg)
