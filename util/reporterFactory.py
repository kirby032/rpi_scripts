'''
XXX: docstring
'''
import logging
import pkgutil

logger = logging.getLogger(__name__)

reportingClasses = {}

for _, name, ispkg in pkgutil.iter_modules(['reporting']):
    if not ispkg and name != 'Reporter':
        tempClass = __import__('reporting', globals(), locals(), [name], -1) \
            .__getattribute__(name).__getattribute__(name)
        reportingClasses[name] = tempClass

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
