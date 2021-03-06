'''
XXX: docstring
'''
import datetime
import logging
from email.mime.text import MIMEText
import smtplib
import socket

from reporting.Reporter import Reporter
import util.config

logger = logging.getLogger(__name__)

CONFIG_KEYS = {
    'CREDENTIALS_KEY': 'credentials_file',
    'EMAIL_FROM_KEY': 'from_address',
    'EMAIL_RECIPIENTS_KEY': 'recipients',
    'LOG_ONLY_KEY': 'log_only',
    'SMTP_DOMAIN_KEY': 'smtp_domain',
    'SMTP_PORT_KEY': 'smtp_port',
    'SUBJECT_KEY': 'subject'
}

class SMTPReporter(Reporter):
    '''
    XXX: docstring
    '''
    def __init__(self, config):
        super(SMTPReporter, self).__init__(config)
        self.smtpConfig = config['data']
        util.config.validateConfig(config.get('data'), CONFIG_KEYS)

    def send(self, msg, event):
        '''
        XXX: docstring
        '''
        message = MIMEText(msg)
        message['Subject'] = str(datetime.date.today()) + ': ' + \
            self.smtpConfig[CONFIG_KEYS['SUBJECT_KEY']]
        message['From'] = self.smtpConfig[CONFIG_KEYS['EMAIL_FROM_KEY']]
        message['To'] = ','.join(
            self.smtpConfig[CONFIG_KEYS['EMAIL_RECIPIENTS_KEY']])

        if self.smtpConfig[CONFIG_KEYS['LOG_ONLY_KEY']]:
            logger.info('SMTPReporter Message:\n%s', message.as_string())
            event.set()
            return

        password = util.config.importConfig(
            self.smtpConfig[CONFIG_KEYS['CREDENTIALS_KEY']])['password']

        try:
            session = smtplib.SMTP(
                self.smtpConfig[CONFIG_KEYS['SMTP_DOMAIN_KEY']],
                self.smtpConfig[CONFIG_KEYS['SMTP_PORT_KEY']], timeout=5)
            session.starttls()
            session.login(self.smtpConfig[CONFIG_KEYS['EMAIL_FROM_KEY']],
                password)
            session.sendmail(self.smtpConfig[CONFIG_KEYS['EMAIL_FROM_KEY']],
                self.smtpConfig[CONFIG_KEYS['EMAIL_RECIPIENTS_KEY']],
                message.as_string())
            session.quit()
        except (socket.error, smtplib.SMTPException) as error:
            logger.error('Failed to send email via SMTP server at %s:%d',
                self.smtpConfig[CONFIG_KEYS['SMTP_DOMAIN_KEY']],
                self.smtpConfig[CONFIG_KEYS['SMTP_PORT_KEY']])
            logger.error('Error: %s', str(error))

        event.set()
