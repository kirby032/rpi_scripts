# pylint: disable=missing-docstring
import collections
import random
import unittest

import mock

from util.classes import Object

class TestReporterFactoryPreImport(unittest.TestCase):
    def setUp(self):
        self.patches = []
        self.reporters = []

        # Import the real module
        self.reporterFactory = __import__(
            'util.reporterFactory', globals(), locals(),
            ['buildReporterFromConfig'], -1)

        # Mock import so reporterFactory can try to import fake modules
        self.real_import = __import__
        p = mock.patch('__builtin__.__import__', side_effect=self.fakeImport)
        self.patches.append(p)
        p.start()

    def tearDown(self):
        for patch in self.patches:
            patch.stop()

    # pylint: disable=dangerous-default-value
    def fakeImport(self, pkgName, _globals=globals(),
            _locals=locals(), _fromlist=[], _level=-1):
        '''
        This function will replace the call to import. We generally want this
        to be a pass through unless the import is specifically for our fake
        reporter modules
        '''
        if pkgName in self.reporters:
            val = Object()
            setattr(val, pkgName[len('reporting.'):], Object())
            setattr(getattr(val, pkgName[len('reporting.'):]),
                pkgName[len('reporting.'):], mock.Mock())
            setattr(getattr(getattr(
                val, pkgName[len('reporting.'):]), pkgName[len('reporting.'):]),
                '__name__', pkgName[len('reporting.'):])
            return val

        return self.real_import(pkgName, _globals, _locals, _fromlist, _level)

    def mockIterModulesWithReporters(self, reporters):
        '''
        Mock out pkgutil.iter_modules to return the passed in set of reporters
        '''
        self.assertTrue(isinstance(reporters, collections.Sequence))

        p = mock.patch('pkgutil.iter_modules',
            return_value=[(None, r, False) for r in reporters])
        self.patches.append(p)
        p.start()

    def createReportersArray(self, numReporters, defaultReporter=True):
        reporters = []
        if defaultReporter:
            reporters.append('Reporter')

        # Of the form 'reporting.My###Reporter'
        self.reporters = ['reporting.My' + str(num) + 'Reporter' \
            for num in range(1, numReporters + 1)]

        # Of the form 'My###Reporter' a 'reporting.' will be prepended by
        # reporterFactory.py when trying to import the modules
        reporters.extend(['My' + str(num) + 'Reporter' \
            for num in range(1, numReporters + 1)])

        return reporters

    def do_test_with_num_reporters(self, numReporters, defaultReporter=True):
        self.mockIterModulesWithReporters(
            self.createReportersArray(numReporters, defaultReporter))
        reload(self.reporterFactory)
        self.assertEqual(len(self.reporterFactory.reportingClasses),
            numReporters)

    def test_no_reporters_defined(self):
        with self.assertRaisesRegexp(KeyError,
                'Could not find Reporter.py. Must have a base class in order ' +
                'to define reporters'):
            self.do_test_with_num_reporters(0, False)

    def test_with_only_base_reporter(self):
        self.do_test_with_num_reporters(0)

    def test_with_random_non_base_reporters(self):
        with self.assertRaisesRegexp(KeyError,
                'Could not find Reporter.py. Must have a base class in order ' +
                'to define reporters'):
            self.do_test_with_num_reporters(random.randint(1, 101), False)

    def test_with_one_other_reporter(self):
        self.do_test_with_num_reporters(1)

    def test_with_random_num_reporters(self):
        self.do_test_with_num_reporters(random.randint(2, 101))

class TestReporterFactoryPostImport(unittest.TestCase):
    def setUp(self):
        self.buildReporterFromConfig = __import__('util.reporterFactory',
            globals(), locals(), ['buildReporterFromConfig'], -1) \
            .__getattribute__('buildReporterFromConfig')

    def test_build_generic_reporter(self):
        with self.assertRaises(KeyError):
            self.buildReporterFromConfig(
                {'type': 'Reporter', 'id': 'myBaseReporter'})

    def test_build_invalid_reporter(self):
        # XXX: Should make this KeyError more explict exception
        with self.assertRaises(KeyError):
            self.buildReporterFromConfig(
                {'type': 'NonExistent', 'id': 'myFakeReporter'})

    def test_build_SMTPReporter(self):
        from reporting.SMTPReporter import SMTPReporter
        reporter = self.buildReporterFromConfig(
            {'type': 'SMTPReporter', 'id': 'emailReporter1', 'data': {
                "credentials_file": "etc/config/SMTPCredentials.cfg",
                "from_address": "mkirbydev.home.automation@gmail.com",
                "recipients": [
                    "michael.kirby032@gmail.com"
                ],
                "smtp_domain": "smtp.gmail.com",
                "smtp_port": 587,
                "subject": "ALERT!!!!!!",
                "log_only": False}})

        self.assertEqual(reporter.id, 'emailReporter1')
        self.assertTrue(isinstance(reporter, SMTPReporter))
