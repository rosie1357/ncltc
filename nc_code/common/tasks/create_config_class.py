import os
from pathlib import Path

from common.classes.ConfigClass import Config
from common.utils.read_config import variable_matcher, variable_constructor

def create_config_class(**kwargs):
    """
    Function create_config_class to read in common config and any additional specified in kwargs to add
    attributes to returned instance
    
    """

    # create empty instance of ConfigClass, add base setup yaml

    ConfigInstance = Config()

    config_path = Path(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'config')))

    ConfigInstance.add_attributes(config_path / 'setup_config.yaml',
                                  variable_match = {'matcher' : variable_matcher, 'constructor' : variable_constructor})

    # add any additional passed in as kwargs, where config name is key and path is value
    # for config_table == tables_config only, assume value is list of [path, table_name], where table_name should be passed as ** to specify
    # only outer key that should be kept in that specific config

    for name, details in kwargs.items():

        ConfigInstance.add_attributes(details['path'] / name, outer_dict = details.get('outer_dict'))

    return ConfigInstance