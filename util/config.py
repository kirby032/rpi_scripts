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
