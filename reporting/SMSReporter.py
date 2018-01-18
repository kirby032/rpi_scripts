'''
XXX: docstring
'''

import logging

from reporting.Reporter import Reporter

logger = logging.getLogger(__name__)


class SMSReporter(Reporter):
    '''
    XXX: docstring
    '''

    def __init__(self, config):
        super(SMSReporter, self).__init__(config)
