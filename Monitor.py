'''
This is the main monitor
'''

import argparse
import logging
import sys

from sensors.Sensor import Sensor

logLevels = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG
    }
logger = logging.getLogger(__name__)

class Monitor(object):
    '''Main class for all monitoring'''

    def __init__(self):
        self.sensor = Sensor('myconfig', 'handler')

    def __str__(self):
        return 'I\'m a monitor'

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

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    setup_logging(args.log_level, args.log_file, args.debug)

    try:
        monitor = Monitor()
        logger.debug('Monitor: %s', str(monitor))
    # pylint: disable=broad-except
    except Exception:
        logger.exception('terminal exception encountered')
