import os
from pathlib import Path

from common.classes.ConfigClass import ConfigClass
from common.utils.read_config import variable_matcher, variable_constructor

def create_config_class():

    ConfigInstance = ConfigClass()

    config_path = Path(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'config')))

    ConfigInstance.add_attributes(config_path / 'setup_config.yaml',
                                  variable_match = {'matcher' : variable_matcher, 'constructor' : variable_constructor})

    return ConfigInstance