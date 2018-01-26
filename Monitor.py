'''
This is the main monitor
'''

import argparse
import logging
import sys
import time
from threading import Thread

import util.config

logLevels = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG
    }
logger = logging.getLogger()

class Monitor(object):
    '''Main class for all monitoring'''

    def __init__(self, config):
        '''
        Constructor for Monitor class

        Args:
            config: JSON config for the Monitor class
        '''
        from util.reporterFactory import buildReporterFromConfig
        from util.sensorFactory import buildSensorFromConfig

        self.config = config
        self.sensors = []
        self.reporters = []
        if 'sensors' in self.config:
            for sensor in self.config['sensors']:
                self.sensors.append(buildSensorFromConfig(sensor,
                    self.sensorTrigger))
        if 'reporters' in self.config:
            for reporter in self.config['reporters']:
                self.reporters.append(buildReporterFromConfig(reporter))

    def sensorTrigger(self, sensor):
        '''
        XXX: docstring
        '''
        logger.info('Sensor %s triggered', sensor)

        msg = 'Sensor {} was triggered!'.format(sensor)

        threads = []
        for reporter in self.reporters:
            thread = Thread(target=reporter.send, args=[msg])
            thread.daemon = True
            thread.start()
            threads.append(thread)

        return threads

    def getSensors(self):
        '''
        XXX: docstring
        '''
        return self.sensors

    def getReporters(self):
        '''
        XXX: docstring
        '''
        return self.reporters

    def __str__(self):
        return 'Monitor w/ {} sensors, {} reporters'.format(
            len(self.sensors), len(self.reporters))

def get_parser():
    '''
    Build program's top level argument parser

    Args:
        none
    Returns:
        parser: The default parser
    '''
    defaultParser = argparse.ArgumentParser(description='parser_description')
    defaultParser.add_argument('--debug', '-d', action='store_true',
        help='enable debug mode which also outputs all logging to stdout')
    defaultParser.add_argument('--config-file', '-c',
        help='specify the config file to use (default: ' +
            '"etc/config/HomeMonitor.cfg"',
        default='etc/config/HomeMonitor.cfg')
    defaultParser.add_argument('--log-file', '-f',
        help='specify log file (default: "monitor.log")',
        default='monitor.log')
    defaultParser.add_argument('--log-level', '-l',
        help='set default log level', choices=logLevels.values(),
        type=lambda val: logLevels[val.upper()], default=logging.WARNING)
    return defaultParser

def setup_logging(logLevel, logFile, debug):
    '''
    Setup default logging

    If @a debug is True then we will create an additional handler to output all
    messages to stdout as well as standard log file

    Args:
        logLevel: Default log level, must be in logLevels dict
        debug: Specifies whether or not we're in debug mode
    Returns:
        none
    '''
    print 'Logging to {}'.format(logFile)
    logger.setLevel(logLevel)
    formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s',
        '%Y-%m-%d %H:%M:%S (%Z)')
    fileHandler = logging.FileHandler(logFile)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    if debug:
        streamHandler = logging.StreamHandler(sys.stdout)
        streamHandler.setFormatter(formatter)
        logger.addHandler(streamHandler)

#def testDriver(mainMonitor):
#    '''
#    Driver for monitor to test functionality
#
#    Args:
#        monitor: An initialized monitor object
#    '''
#    from sensors.MagSwitchSensor import MagSwitchSensor
#    for sensor in mainMonitor.getSensors():
#        logger.warning('%s', str(sensor))
#        if isinstance(sensor, MagSwitchSensor):
#            sensor.setSwitchState(1)
#            sensor.setSwitchState(0)
#            time.sleep(6)
#            sensor.setSwitchState(1)
#
#    for reporter in mainMonitor.getReporters():
#        logger.warning('%s', str(reporter))

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    setup_logging(args.log_level, args.log_file, args.debug)

    try:
        monitor = Monitor(util.config.importConfig(args.config_file))
        while 1:
            time.sleep(100)
    # pylint: disable=broad-except
    except Exception:
        logger.exception('terminal exception encountered')
