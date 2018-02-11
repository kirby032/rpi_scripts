'''
XXX: docstring
'''
import logging
import time

from sensors.Sensor import Sensor
import util.config

logger = logging.getLogger(__name__)
platform = ''
try:
    # pylint: disable=wrong-import-position
    import RPi.GPIO as GPIO
    platform = 'rpi'
    logger.info(
        'Detected Raspberry PI platform so using real MagSwitchSensor')
except ImportError:
    logger.info(
        'Detected non Raspberry PI platform so using mock MagSwitchSensor')

CONFIG_KEYS = {
    'EDGE_TYPE_KEY': 'edge_type',
    'DELAY_KEY': 'delay',
    'INPUT_PIN_KEY': 'input_pin'
}

class MagSwitchSensor(Sensor):
    '''
    XXX: docstring
    '''
    def __init__(self, config, triggerHandler):
        super(MagSwitchSensor, self).__init__(config, triggerHandler)
        util.config.validateConfig(config.get('data'), CONFIG_KEYS)
        self.config = config['data']
        self.triggerHandler = triggerHandler
        self.lastTrigger = 0

        if self.config[CONFIG_KEYS['EDGE_TYPE_KEY']].upper() == 'RISING':
            self.isRisingEdgeDetected = True
        elif self.config[CONFIG_KEYS['EDGE_TYPE_KEY']].upper() == 'FALLING':
            self.isRisingEdgeDetected = False
        else:
            logger.error('%s in config file had unexpected value \'%s\'',
                CONFIG_KEYS['EDGE_TYPE_KEY'],
                self.config[CONFIG_KEYS['EDGE_TYPE_KEY']])
            logger.error('Expected either \'RISING\' or \'FALLING\'')

        if platform != 'rpi':
            self.state = 0 if self.isRisingEdgeDetected else 1
            return

        # Set up for BCM pin numbering scheme
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.config[CONFIG_KEYS['INPUT_PIN_KEY']], GPIO.IN,
            pull_up_down=(
                GPIO.PUD_DOWN if self.isRisingEdgeDetected else GPIO.PUD_UP))
        GPIO.add_event_detect(self.config[CONFIG_KEYS['INPUT_PIN_KEY']],
            GPIO.RISING if self.isRisingEdgeDetected else GPIO.FALLING,
            callback=self.trigger)

        logger.debug('Setup up MagSwitchSensor on pin %d for %s edge trigger',
            self.config[CONFIG_KEYS['INPUT_PIN_KEY']],
            'RISING' if self.isRisingEdgeDetected else 'FALLING')

    def trigger(self, _):
        '''
        XXX: docstring
        '''
        currentTime = time.time()
        if currentTime - self.lastTrigger >= \
                self.config[CONFIG_KEYS['DELAY_KEY']]:
            logger.debug('MagSwitchSensor %s triggered!', self.id)
            self.lastTrigger = time.time()
            self.triggerHandler(self)
            return
        else:
            logger.debug('Sensor %s triggered but had not achieved long ' +
                'enough delay', str(self))
            logger.debug('CurrentTime: %d', currentTime)
            logger.debug('LastTrigger: %d', self.lastTrigger)
            logger.debug('Delay: %d', self.config[CONFIG_KEYS['DELAY_KEY']])

    def setSwitchState(self, state):
        '''
        XXX: docstring
        '''
        if self.state != state and bool(state) == self.isRisingEdgeDetected:
            self.trigger(self.config[CONFIG_KEYS['INPUT_PIN_KEY']])
        self.state = state
