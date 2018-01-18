'''
XXX: docstring
'''

import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
#import mimetypes

# pylint: disable=import-error
import apiclient.discovery
# pylint: disable=import-error
import apiclient.errors
import httplib2
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from reporting.Reporter import Reporter


logger = logging.getLogger(__name__)

CLIENT_SECRET_KEY = 'client_secret'
CREDENTIALS_CACHE_KEY = 'credentials_cache'
EMAIL_ACCT_KEY = 'from_address'
EMAIL_RECIPIENTS_KEY = 'recipients'

SCOPES = 'https://www.googleapis.com/auth/gmail.send'

class SMTPReporter(Reporter):
    '''
    XXX: docstring
    '''

    def __init__(self, config):
        super(SMTPReporter, self).__init__(config)
        self.store = Storage(self.config[CREDENTIALS_CACHE_KEY])

    def _getCredentials(self):
        '''
        XXX: docstring
        '''
        creds = self.store.get()
        try:
            if not creds or creds.invalid:
                flow = client.flow_from_clientsecrets(
                    self.config[CLIENT_SECRET_KEY], SCOPES)
                flow.run_console()
                #flow.user_agent = 'HomeMonitor'
                #creds = tools.run_flow(flow, self.store,
                #        {
                #            "noauth_local_webserver": True,
                #            "logging_level": logger.getEffectiveLevel()
                #        })
        # XXX: Remove this pylint exception
        # pylint: disable=bare-except
        except client.Error as error:
            logger.error('Failed to get google creds!!')
            logger.error('Error: %s', str(error))

        return creds

    def _buildMessage(self, msg):
        '''
        XXX: docstring
        '''
        # XXX: why 'alternative'?
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'We\'re under attack'
        msg['From'] = self.config[EMAIL_ACCT_KEY]
        msg['To'] = ', '.join(self.config[EMAIL_RECIPIENTS_KEY])
        msg.attach(MIMEText(msg, 'plain'))

        return {'raw': base64.urlsafe_b64encode(msg.as_string())}

    def send(self, msg):
        '''
        XXX: docstring
        '''
        logger.warning('Sending email: %s', msg)
        creds = self._getCredentials()
        http = creds.authorize(httplib2.Http())
        service = apiclient.discovery.build('gmail', 'v1', http=http)
        fullMsg = self._buildMessage(msg)
        try:
            service.users().messages().send(userId='me', body=fullMsg).execute()
        except apiclient.errors.HttpError as error:
            logger.error('An error occurred sending email to %s',
                ', '.join(self.config[EMAIL_RECIPIENTS_KEY]))
            logger.error('Error: %s', str(error))
            return False

        return True
