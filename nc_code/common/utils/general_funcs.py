import logging
import time
import tempfile
import os
from pathlib import Path
import inspect

def print_df_to_log(*, log, df, message, print_index=False):
    """
    Function print_to_log to print message and an input df to log
    
    params:
        log logger obj: log to write to
        df df: df to print after message (will print all input records/columns)  
        message str: message to print
        print_index boolean: boolean to write index when printing df - default is False (does not print index)
    
    returns:
        none
    
    """
    
    log.info(f"\n{message}:\n")
    log.info(f"{df.to_string(index=print_index)}") 

def generate_logger(*, logdir=None, logname, packages_suppress = ['boto3','botocore','numexpr'], suppress_addtl = [], init_message = None):
    """
    Function generate_logger to generate log file for given directory and log name. Sets level to INFO
    
    params:
        logdir Path or None: directory for log file, if not specified, assume temp file created
        logname str: name of log file, will add datetime stamp to end of name
        packages_suppress list: default list of packages to set logging level to critical to prevent notes to log
        suppress_addtl list: additional packages to suppress, default is none
        init_message str: optional initial message to write to log, default is none
        
    returns:
        logger

    """

    if logdir == None:
        fd, fname = tempfile.mkstemp()
        logdir = Path(os.path.dirname(fname))
    
    logging.basicConfig(filename=logdir / f'{logname}_{time.strftime("%Y%m%d-%H%M%S")}.log', filemode='w', level=logging.INFO, format='%(message)s')
    
    # for given packages to suppress, set levels to critical
    
    for package in packages_suppress + suppress_addtl:
        logging.getLogger(package).setLevel(logging.CRITICAL)
        
    if init_message is not None:
        logging.info(f"{init_message}\n")
    
    return logging

def get_absolute_path(module, *args):
    """
    Function get_absolute_path to return the absolute path to a given folder in a module
    params:
        module obj: name of base module, e.g. common (must be imported in script when passed to function)
        args: individual names of all subdirectories to append to module main path, e.g. 'tasks', 'read_file'

    returns:
        path: path to folder
    """

    return Path(inspect.getfile(module)).parent / "\\".join(args)

def get_intersection(lst1, lst2):
    """
    Function get_intersection to return the intersection (overlap) of two lists
    params:
        lst1: list
        list2: list

    returns:
        list with intersection of unique elements
    """
    return list(set(lst1) & set(lst2))