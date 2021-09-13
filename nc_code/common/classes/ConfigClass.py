"""
    code to generate a config class to be imported into any module to easily access all elements of config
"""

from common.utils.read_config import read_config

class Config(object):

    def __init__(self):
        pass


    def add_attributes(self, config_path, outer_dict = None, **kwargs):
        """
            Method to add attributes to class instance by reading in config yaml file and
            adding each item in config dict as attribute
            params:
                config_path Path: path to config file to read in/parse
                outer_dict str/num (Optional): optional param to pass if yaml file is surrounded by main outer dictionary
                    to exclude when assigning attributes
                kwargs dict: optional dictionary to pass constructors to read_config - see read_config doc for more info
        
        """
        
        config = read_config(config_path, **kwargs)
        if outer_dict:
            config = config[outer_dict]

        for key, value in config.items():
            setattr(self, key, value)