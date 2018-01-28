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
        # pylint: disable=useless-super-delegation
        super(SMSReporter, self).__init__(config)
