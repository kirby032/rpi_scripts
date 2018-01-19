'''
XXX: docstring
'''

import logging
from email.mime.text import MIMEText
import smtplib
import socket

from reporting.Reporter import Reporter
import util.config

logger = logging.getLogger(__name__)

CREDENTIALS_KEY = 'credentials_file'
EMAIL_FROM_KEY = 'from_address'
EMAIL_RECIPIENTS_KEY = 'recipients'
LOG_ONLY_KEY = 'log_only'
SMTP_DOMAIN_KEY = 'smtp_domain'
SMTP_PORT_KEY = 'smtp_port'
SUBJECT_KEY = 'subject'

class SMTPReporter(Reporter):
    '''
    XXX: docstring
    '''

    def __init__(self, config):
        super(SMTPReporter, self).__init__(config)
        self.smtpConfig = config['data']

    def send(self, msg):
        '''
        XXX: docstring
        '''
        message = MIMEText(msg)
        message['Subject'] = self.smtpConfig[SUBJECT_KEY]
        message['From'] = self.smtpConfig[EMAIL_FROM_KEY]
        message['To'] = ','.join(self.smtpConfig[EMAIL_RECIPIENTS_KEY])

        if self.smtpConfig[LOG_ONLY_KEY]:
            logger.warning('SMTPReporter Message:\n%s', message.as_string())
            return

        password = util.config.importConfig(
            self.smtpConfig[CREDENTIALS_KEY])['password']

        try:
            session = smtplib.SMTP(self.smtpConfig[SMTP_DOMAIN_KEY],
                self.smtpConfig[SMTP_PORT_KEY], timeout=5)
            session.starttls()
            session.login(self.smtpConfig[EMAIL_FROM_KEY],
                password)
            session.sendmail(self.smtpConfig[EMAIL_FROM_KEY],
                self.smtpConfig[EMAIL_RECIPIENTS_KEY], message.as_string())
            session.quit()
        except (socket.error, smtplib.SMTPException) as error:
            logger.error('Failed to send email via SMTP server at %s:%d',
                self.smtpConfig[SMTP_DOMAIN_KEY],
                self.smtpConfig[SMTP_PORT_KEY])
            logger.error('Error: %s', str(error))
            raise
