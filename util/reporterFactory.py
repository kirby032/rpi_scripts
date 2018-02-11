'''
XXX: docstring
'''
import logging
import pkgutil

logger = logging.getLogger(__name__)

reportingClasses = {}

foundBaseClass = False
for _, name, ispkg in pkgutil.iter_modules(['reporting']):
    if name == 'Reporter':
        foundBaseClass = True
        continue
    # If it is a package and not a test file:
    if not ispkg and name[-5:] != '_test':
        tempClass = __import__('reporting.' + name, globals(), locals(), [],
            -1).__getattribute__(name).__getattribute__(name)
        reportingClasses[name] = tempClass

if not foundBaseClass:
    raise KeyError('Could not find Reporter.py. Must have a base class in ' +
        'order to define reporters')

logger.info('Found %d reporter classes', len(reportingClasses))
if logger.isEnabledFor(logging.DEBUG):
    logger.debug('Reporter Classes:')
    for reporterClass in reportingClasses:
        logger.debug('\t%s', reportingClasses[reporterClass].__name__)

def buildReporterFromConfig(config):
    '''
    Reads the config for the type of reporter and instantiates that type

    Args:
        config: The configuration dict for this reporter

    Returns:
        reporter: The reporter of the appropriate class as indicated by the
            config
    '''
    return reportingClasses[config['type']](config)
