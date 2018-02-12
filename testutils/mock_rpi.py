'''
XXX: docstring
'''
import logging
import sys

from util.classes import Object

log = logging.getLogger(__name__)

pins = {}

mono_id = 0

def gen_trigger_id():
    '''
    XXX: docstring
    '''
    # pylint: disable=global-statement
    global mono_id
    mono_id += 1
    return mono_id

def add_pin(pin):
    '''
    XXX: docstring
    '''
    pins[pin] = {}
    pins[pin]['triggers'] = {}
    pins[pin]['state'] = None

def set_pin_state(pin, state):
    '''
    XXX: docstring
    '''
    events = []

    if pin not in pins:
        add_pin(pin)
    elif state != pins[pin]['state']:
        for _, (mode, callback) in pins[pin]['triggers'].iteritems():
            if state == mode:
                events.extend(callback(pin))

    pins[pin]['state'] = state

    return events

class fakeGPIO(object):
    '''
    XXX: docstring
    '''
    BCM = 'mode'
    IN = 'in'
    OUT = 'out'
    RISING = 1
    FALLING = 0

    class PinNotInitializedError(ValueError):
        '''
        XXX: docstring
        '''
        pass

    def __init__(self):
        self.trigger_ids = []

    def __del__(self):
        for trigger_id, pin in self.trigger_ids:
            del pins[pin]['triggers'][trigger_id]

    def setmode(self, mode):
        '''
        XXX: docstring
        '''
        pass

    # pylint: disable=no-self-use
    def setup(self, pin, direction):
        '''
        XXX: docstring
        '''
        if pin not in pins:
            add_pin(pin)
        pins[pin]['direction'] = direction

    def add_event_detect(self, pin, mode, callback):
        '''
        XXX: docstring
        '''
        if pin not in pins:
            raise fakeGPIO.PinNotInitializedError(
                'Pin {} not initialized!'.format(pin))

        trigger_id = gen_trigger_id()
        self.trigger_ids.append((trigger_id, pin))
        pins[pin]['triggers'].update({trigger_id: (mode, callback)})


fakePackage = Object()
fakePackage.GPIO = fakeGPIO()
sys.modules['RPi'] = fakePackage
sys.modules['RPi.GPIO'] = Object()
