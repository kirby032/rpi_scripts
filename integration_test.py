# pylint: disable=missing-docstring
from collections import namedtuple
import unittest

import mock

import testutils.mock_rpi as rpi

from Monitor import Monitor
import util.config

Email = namedtuple('Email', ['from_address', 'to_addresses', 'message'])

class TestEndToEnd(unittest.TestCase):
    def append_email(self, from_address, to_address, message):
        self.emails.append(Email(from_address, to_address, message))

    def setUp(self):
        self.patches = []
        self.emails = []
        patch = mock.patch('smtplib.SMTP.sendmail',
            side_effect=self.append_email)
        patch.start()
        self.patches.append(patch)

        rpi.set_pin_state(26, 0)
        config_file = 'etc/config/HomeMonitor.cfg'

        self.monitor = Monitor(util.config.importConfig(config_file))

    def tearDown(self):
        for patch in self.patches:
            patch.stop()

    def testDoorOpenOnce(self):
        # Simulate a door opening
        events = rpi.set_pin_state(26, 1)

        # Wait for async reporting
        for event in events:
            event.wait()

        self.assertEqual(1, len(self.emails))
        email = self.emails[0]
        self.assertEqual(['michael.kirby032@gmail.com'], email.to_addresses)
        self.assertEqual('mkirbydev.home.automation@gmail.com',
            email.from_address)
