"""
Functions to read NC config.yaml
"""

import yaml
import re
from common.config.base_dir import BASE_DIR

# define variable_matcher to be passed to yaml.add_implicit_resolver to match pattern of ${} in yaml load to
# identify variables to resolve

variable_matcher = re.compile(r'\$\{(\w+)\}')

def variable_constructor(loader, node):
    """
    Function variable_constructor to be passed to yaml.add_constructor to extract variable names from passed
    yaml params and return variable value
    """

    value = node.value
    match = variable_matcher.findall(value)

    if match:
        for g in match:
            value = value.replace(
                f'${{{g}}}', eval(g)
            )

    return value

def read_config(config_path, **kwargs):
    """
    Function read_config to read yaml config file and return file after conversion to python object
    
    params:
        config_path Path: path to config file

        kwargs dict: optional dictionary to pass constructors to add to yaml if needed,
            must be passed in form of constructor name as key, then values of matcher and constructor equal to match and construct functions
            example: 
                variable_match = {'matcher' : variable_matcher, 'constructor' : variable_constructor}
                where variable_matcher is regex compiler to match expression, variable_constructor is function to return evaluated matched group 0
    
    returns:
        dict: dictionary of input yaml config file
    """
    
    # if matcher and constructor dict passed in kwargs, add to yaml reader
    
    for construct_name, values in kwargs.items():
    
        yaml.add_implicit_resolver(construct_name, values['matcher'], None, yaml.SafeLoader)
        yaml.add_constructor(construct_name, values['constructor'], yaml.SafeLoader)

    with open(config_path) as f:
        config = yaml.safe_load(f)

    return config