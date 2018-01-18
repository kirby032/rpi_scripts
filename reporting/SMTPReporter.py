'''
XXX: docstring
'''

import logging

from reporting.Reporter import Reporter

logger = logging.getLogger(__name__)

class SMTPReporter(Reporter):
    '''
    XXX: docstring
    '''

    def __init__(self, config):
        super(SMTPReporter, self).__init__(config)
