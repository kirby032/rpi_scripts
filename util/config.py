'''
Utilities for working with configuration
'''

import json

def importConfig(configFile):
    '''
    Converts a JSON configuration file to a dictionary of settings

    Args:
        configFile: String that represents the file's path

    Returns:
        config: Dictionary of settings read from the json file
    '''
    config = {}

    with open(configFile, 'r') as f:
        config = json.load(f)

    return config

def validateConfig(config, keys):
    '''
    XXX: Docstring
    '''
    if keys is None or len(keys) == 0:
        return True

    if config is None:
        raise ConfigKeyMissingError('Attempted to validate empty config!')

    for key in keys:
        if config.get(keys[key]) is None:
            raise ConfigKeyMissingError('Key {}({}) not found in config {}'
                .format(key, keys[key], config))

    return True


class ConfigKeyMissingError(Exception):
    '''
    XXX: Docstring
    '''
    pass

